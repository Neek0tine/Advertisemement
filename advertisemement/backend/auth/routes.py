import glob
import re
import os, sys
from . import app, db
from numerize import numerize 
from .dbmodel import Coder, Codes, Posts, Profiles
from flask import render_template, redirect, url_for, session, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, RadioField
from wtforms.validators import InputRequired, DataRequired
from collections import deque
import jsonify
from sqlalchemy.exc import NoResultFound, MultipleResultsFound


def shorten_number(number_to_shorten):
    """
    Shorten number to thousands (K), Millions (M). You get the idea

    Args:
        number_to_shorten (int): The number. Ex. 21084901

    Returns:
        str: The shortened numbers. Ex. 21M
    """
    return str(numerize.numerize(number_to_shorten))

# Forms
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    submit = SubmitField('submit')

class CategorizationForm(FlaskForm):
    post_id = HiddenField('Post ID', validators=[DataRequired()])
    number_of_memes = RadioField('Number of Memes', choices=[(0, 'None'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, 'More than 5')], coerce=int, validators=[InputRequired()])
    type_of_memes = RadioField('Type of Memes', choices=[(0, 'None'), (1, 'Textual'), (2, 'Visual'), (3, 'Auditory'), (4, 'Textual and Visual'), (5, 'Visual and Auditory'), (6, 'Textual and Auditory'), (7, 'Textual, Visual and Auditory')], coerce=int, validators=[InputRequired()])
    type_of_movement = RadioField('Type of Movement', choices=[(1, 'None'), (2, 'Physical'), (3, 'Causal'), (4, 'Emotional'), (5, 'Physical and causal'), (6, 'Physical and emotional'), (7, 'Physical, causal and emotional')], coerce=int, validators=[InputRequired()])
    type_of_emotions = RadioField('Type of Emotions', choices=[(1, 'Positive'), (2, 'Neutral'), (3, 'Negative')], coerce=int, validators=[InputRequired()])
    type_of_subject = RadioField('Type of Subject', choices=[(1, 'Character'), (2, 'Object'), (3, 'Creature'), (4, 'Scene')], coerce=int, validators=[InputRequired()])
    submit = SubmitField('Next')

@app.route('/')
def home():
    """
    Root address. Currently used to checks whether a user is logged in

    """

    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if form.validate_on_submit():
        print('[+] Form validated', file=sys.stderr)
        coder = Coder.query.filter_by(username=form.username.data).first()
        if coder:
            print("[+] Logged in successfully, user: " + str(form.username.data), file=sys.stderr)
            login_user(coder)
            
            print(f'\n =========== [!] Relogging-in. All variables are reset. =========== ')
            session['current_post_id'] = Posts.query.order_by(db.func.rand()).first().id
            session['previous_posts'] = deque([], maxlen=25)
            session['next_posts'] =  deque([], maxlen=25)
            session['custom_userprofile'] = None    
            return redirect(url_for('dashboard'))
        
    # flash('Email atau Password salah, mohon periksa ulang!', 'danger')
    print("[-] Login failed " + str(form.username.data), form.data, file=sys.stderr)
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = CategorizationForm()
    print(f'\n[+] Previously = {session["previous_posts"]} ', file=sys.stderr)
    print(f'\n[+] Next = {session["next_posts"]}', file=sys.stderr)

    try:
        print(f'\n[+] Brand = {session["custom_userprofile"]}', file=sys.stderr)
    except KeyError:
        print(f'\n[+] No brand selected', file=sys.stderr)




    def fill_form(code):
        """
        Fill in the forms in the dashboard

        :return: None/ True if done
        """ 
        form.number_of_memes.data = code.number_of_memes
        form.type_of_memes.data = code.type_of_memes
        form.type_of_movement.data = code.type_of_movement
        form.type_of_emotions.data = code.type_of_emotions
        form.type_of_subject.data = code.type_of_subject
        
    def empty_form():
        """
        Fill in the forms in the dashboard

        :return: None/ True if done
        """ 
        form.number_of_memes.data = ""
        form.type_of_memes.data = ""
        form.type_of_movement.data = ""
        form.type_of_emotions.data = ""
        form.type_of_subject.data = ""

    def get_form():
        """
        Get, add and commit the form input from the dashboard. Not validated yet.

        :return: CategorizedPost, db object to be added
        """ 

        categorized_post = Codes(
            user_id=current_user.id,
            post_id=form.post_id.data,
            number_of_memes=form.number_of_memes.data,
            type_of_memes=form.type_of_memes.data,
            type_of_movement=form.type_of_movement.data,
            type_of_emotions=form.type_of_emotions.data,
            type_of_subject=form.type_of_subject.data,
        )
        
        return categorized_post

    def code_exists(post_id, user_id):
        """Returns true (and the code) if a code is found. 

        Args:
            post_id (int): Post id, Posts.id or Codes.post_id
            user_id (int): User id, Coder.id or Codes.user_id

        Returns:
            post_exist: db query
            bool: True if exists
        """
        try:
            code_exist = Codes.query.filter_by(user_id=user_id, post_id = post_id).one()
            return code_exist
        except NoResultFound:
            return False
        except MultipleResultsFound:
            latest_code = Codes.query.filter_by(user_id=user_id, post_id = post_id).first()
            db.session.delete(latest_code)
            code_exists(post_id=post_id, user_id=user_id)
        

    def post_exists(post_id):
        """Returns true (and the post) if a post is found. 

        Args:
            post_id (int): Post id, Posts.id or Codes.post_id

        Returns:
            bool: True if exists
        """

        try:
            post_exist = db.session.query(Posts.id).filter_by(id=post_id).one()
            return True
        except NoResultFound:
            flash('Post with such ID was not found.')
            return False
    
    def show_media(post_id):
        print(f'\n[!] Showing Media: {post_id}\n')
        """
        Returns media and some metadata

        :post: a post record queried from Posts table as a whole
        :return: caption, followers, likes, media_file, media_type
        """ 

        try:
            post = Posts.query.filter_by(id=post_id).one()
        except NoResultFound:
            print(f'[!]No result found!')
            post = Posts.query.filter_by(id=4737).one()
        
        code = code_exists(post_id, current_user.id)
        print(f'\n[!] Code exist! Media: {post_id}\n')

        if code:
            fill_form(code=code)
        elif not code:
            empty_form()
            
        post_dir = post.local_download_directory

        # // a hack, change directory //
        
        post_dir = (post_dir.split('\\'))[8::]
        post_dir = str('C:/Users/nicho/Documents/Thesis/Advertisemement/advertisemement/frontend/templates/assets/img/' + '/'.join(post_dir))
        # print(post_dir)

        video_files = glob.glob(os.path.join(post_dir, '*.mp4'))
        # print(video_files)
        image_files = glob.glob(os.path.join(post_dir, '*.jpg')) + glob.glob(os.path.join(post_dir, '*.png'))
        # print(image_files)

        media_file = None
        media_type = None

        if video_files:
            media_file = video_files[0]
            media_type = 'video'
        
        elif image_files:
            media_file = image_files[0]
            media_type = 'image'

        
        media_file = media_file.split('/')
        media_file = media_file[9::]
        print(media_file)
        media_file = str('/'.join(media_file))
        
        # media_file = str(post_dir + '/' + media_file)
        
        form.post_id.data = post.id

        likes = shorten_number(post.likes)
        followers = shorten_number(db.session.query(Profiles.followers).filter(Profiles.id == post.profile_id).scalar())
        caption = re.sub(r'(\r\n){2,}','\r\n', str(post.caption).strip())
        return post, caption, followers, likes, media_file, media_type
    
    def next():

        try:
            print('[+] Custom user selected:',session['custom_userprofile'], file=sys.stderr)
            if len(session['next_posts']) == 0:

                # new_rand = Posts.query.filter_by(username=session["custom_userprofile"]).order_by(db.func.rand()).first()
                if current_user.username == 'neeko':
                    if session['custom_userprofile'] is None:
                        new_rand = (db.session.query(Posts.id)
                        .outerjoin(Codes, Posts.id == Codes.post_id)
                        .filter(Codes.post_id == None)
                        .order_by(db.func.random())
                        .first())

                    elif session['custom_userprofile'] is not None:
                        new_rand = (db.session.query(Posts.id)
                        .outerjoin(Codes, Posts.id == Codes.post_id)
                        .filter(Codes.post_id == None, Posts.username == session["custom_userprofile"])
                        .order_by(db.func.random())
                        .first())

                elif current_user.username == 'preview':

                    if session['custom_userprofile'] is None:
                        new_rand = (
                            db.session.query(Posts.id)
                            .order_by(db.func.random())
                            .first()
                        )
                    elif session['custom_userprofile'] is not None:
                        new_rand = (
                            db.session.query(Posts.id)
                            .filter(Posts.username == session["custom_userprofile"])
                            .order_by(db.func.random())
                            .first()
                        )
                        print(new_rand)

                elif current_user.username != 'neeko':

                    if session['custom_userprofile'] is None:
                        new_rand = (
                            db.session.query(Posts.id)
                            .join(Codes, Posts.id == Codes.post_id)
                            .filter(Codes.user_id == 1)
                            .order_by(db.func.random())
                            .all()
                        )

                    elif session['custom_userprofile'] is not None:
                        new_rand = (
                            db.session.query(Posts.id)
                            .join(Codes, Posts.id == Codes.post_id)
                            .filter(Codes.user_id == 1, Posts.username == session["custom_userprofile"])
                            .order_by(db.func.random())
                            .all()
                        )
                
                try:
                    session['previous_posts'].append(session['current_post_id'])
                    session['current_post_id'] = new_rand.id
                except:
                    print('[!] All posts has been coded!')      
                    render_template('thankyou.html')


            elif len(session['next_posts']) > 0:
                session['previous_posts'].append(session['current_post_id'])
                session['current_post_id'] = session['next_posts'].popleft()

        except KeyError:
            if len(session['next_posts']) == 0:
                new_rand = Posts.query.order_by(db.func.rand()).first()
                session['previous_posts'].append(session['current_post_id'])
                session['current_post_id'] = new_rand.id

            elif len(session['next_posts']) > 0:
                session['previous_posts'].append(session['current_post_id'])
                session['current_post_id'] = session['next_posts'].popleft()
                
        

            return redirect(url_for('dashboard'))
    
    def previous():
        if len(session['previous_posts']) == 0:
            flash('No previous post found')
            pass

        elif len(session['previous_posts']) > 0:
            session['next_posts'].appendleft(session['current_post_id'])
            session['current_post_id'] = session['previous_posts'].pop()
        return redirect(url_for('dashboard'))

    set_user = request.args.get('userid_input')

    if set_user:
        print('[!] Custom user selected:', set_user, file=sys.stderr)
        session['custom_userprofile'] = set_user
        next()
    elif set_user == '':
        print('[!] Custom user selected reset', file=sys.stderr)
        session.pop('custom_userprofile', None)
        next()

    get_post = request.args.get('postid_input')

    if get_post and post_exists(get_post):
        print('[!] Custom post selected:', get_post, file=sys.stderr)
        session['current_post_id'] = get_post
        return redirect(url_for('dashboard'))
    else:
        pass

    if request.method == 'POST' and form.validate_on_submit() and 'next' in request.form:
        new_code = get_form()
        old_code = code_exists(session['current_post_id'], current_user.id)

        if old_code:
            db.session.delete(old_code)
            db.session.commit()
            db.session.add(new_code)
            db.session.commit()
            
        elif not old_code:
            db.session.add(new_code)
            db.session.commit()

        next()


    elif request.method == 'POST' and form.validate_on_submit() and 'previous' in request.form:
        new_code = get_form()
        old_code = code_exists(session['current_post_id'], current_user.id)

        if old_code:
            db.session.delete(old_code)
            db.session.add(new_code)
            db.session.commit()
        elif not old_code:
            db.session.add(new_code)
            db.session.commit()

        previous()

    elif request.method == 'POST' and 'next' in request.form:
        next()

    elif request.method == 'POST' and 'previous' in request.form:
        previous()
    
    
    post, caption, followers, likes, media_file, media_type = show_media(session['current_post_id'])
    return render_template('dashboard.html', 
                           post=post, 
                           caption = caption, 
                           followers=followers, 
                           likes=likes, 
                           form=form, 
                           media_file=media_file, 
                           media_type=media_type)

@app.route('/logout')
def logout():
    session['previous_steps'] = 0
    logout_user()
    return redirect(url_for('login'))


@app.route('/codebook')
def codebook():
    return render_template('codebook.html')
