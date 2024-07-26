import glob
import re
import os, sys
from . import app, db
from .dbmodel import Coder, Codes, Posts, Profiles
from flask import render_template, redirect, url_for, flash, session, request
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, RadioField
from wtforms.validators import InputRequired, DataRequired
from sqlalchemy.exc import NoResultFound

def shorten_number(number_to_shorten):
            from numerize import numerize 
            return str(numerize.numerize(number_to_shorten))

# Forms
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    submit = SubmitField('submit')

class CategorizationForm(FlaskForm):
    post_id = HiddenField('Post ID', validators=[DataRequired()])
    number_of_panels = RadioField('Number of Panels', choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, 'More than 6')], validators=[DataRequired()])
    type_of_image = RadioField('Type of Image', choices=[(1, 'Photo'), (2, 'Screenshot'), (3, 'Illustration')], validators=[DataRequired()])
    type_of_movement = RadioField('Type of Movement', choices=[(1, 'None'), (2, 'Physical'), (3, 'Causal'), (4, 'Emotional'), (5, 'Physical and Causal'), (6, 'Physical, Causal and Emotional')], validators=[DataRequired()])
    type_of_attribute = RadioField('Type of Attribute', choices=[(1, 'Character'), (2, 'Object'), (3, 'Creature'), (4, 'Scene'), (5, 'Screenshot')], validators=[DataRequired()])
    type_of_emotions = RadioField('Type of Emotions', choices=[(1, 'Positive'), (2, 'Neutral'), (3, 'Negative')], validators=[DataRequired()])
    type_of_subject = RadioField('Type of Subject', choices=[(1, 'Character'), (2, 'Object'), (3, 'Creature'), (4, 'Scene')], validators=[DataRequired()])
    text_existence = RadioField('Text Existence', choices=[(1, 'Yes'), (2, 'No')], validators=[DataRequired()])
    type_of_audience = RadioField('Type of Audience', choices=[(1, 'General'), (2, 'Specific')], validators=[DataRequired()])
    submit = SubmitField('Next')

@app.route('/')
def home():
    if current_user.is_authenticated:
        session['previous_steps'] = 0
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        print('[+] Form validated', file=sys.stderr)
        coder = Coder.query.filter_by(username=form.username.data).first()
        if coder:
            print("[+] Logged in successfully, user: " + str(form.username.data), file=sys.stderr)
            login_user(coder)
            return redirect(url_for('dashboard'))
        # flash('Email atau Password salah, mohon periksa ulang!', 'danger')
    print("[-] Login failed " + str(form.username.data), file=sys.stderr)
    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = CategorizationForm()
    current_post_id = session.get('current_post_id')
    print(f'[+] Step {session['previous_steps']}, expected post ID {current_post_id}', file=sys.stderr)
    post = Posts.query.get(current_post_id)

    if session['previous_steps'] > 0:
        next_codes = Codes.query.filter_by(user_id=current_user.id).order_by(Codes.id.desc()).offset(int(session['previous_steps'])).first()
        current_post_id = session['current_post_id'] = next_codes.post_id
        post = Posts.query.get(current_post_id)
        form.number_of_panels.data = next_codes.number_of_panels
        form.type_of_image.data = next_codes.type_of_image
        form.type_of_movement.data = next_codes.type_of_movement
        form.type_of_attribute.data = next_codes.type_of_attribute
        form.type_of_emotions.data = next_codes.type_of_emotions
        form.type_of_subject.data = next_codes.type_of_subject
        form.text_existence.data = next_codes.text_existence
        form.type_of_audience.data = next_codes.type_of_audience

    if request.method == 'POST' and session['previous_steps'] == 0 and form.validate_on_submit() and 'next' in request.form:
        categorized_post = Codes(
            user_id=current_user.id,
            post_id=form.post_id.data,
            number_of_panels=form.number_of_panels.data,
            type_of_image=form.type_of_image.data,
            type_of_movement=form.type_of_movement.data,
            type_of_attribute=form.type_of_attribute.data,
            type_of_emotions=form.type_of_emotions.data,
            type_of_subject=form.type_of_subject.data,
            text_existence=form.text_existence.data,
            type_of_audience=form.type_of_audience.data,
        )
        
        try:
            exists = Codes.query.filter_by(user_id=current_user.id, post_id = form.post_id.data).one()
            print('[+] Updating post ID', current_post_id) 
            db.session.delete(exists)
            db.session.add(categorized_post)
            db.session.commit()
            session.pop('current_post_id', None)
            post = Posts.query.order_by(db.func.rand()).first()
            session['current_post_id'] = post.id
            return redirect(url_for('dashboard'))
        
        except NoResultFound:
            print('[+] Form Posted!') 
            db.session.add(categorized_post)
            db.session.commit()
            session.pop('current_post_id', None)
            post = Posts.query.order_by(db.func.rand()).first()
            session['current_post_id'] = post.id

        return redirect(url_for('dashboard'))
    
    if request.method == 'POST' and session['previous_steps'] > 0 and form.validate_on_submit() and 'next' in request.form:
        session['previous_steps'] -= 1
        return redirect(url_for('dashboard'))

    if request.method == 'POST' and 'previous' in request.form:
        previous_codes = Codes.query.filter_by(user_id=current_user.id).order_by(Codes.id.desc()).offset(int(session['previous_steps'])).first()
        post = Posts.query.get(previous_codes.post_id)
        session['current_post_id'] = previous_codes.post_id
        form.number_of_panels.data = previous_codes.number_of_panels
        form.type_of_image.data = previous_codes.type_of_image
        form.type_of_movement.data = previous_codes.type_of_movement
        form.type_of_attribute.data = previous_codes.type_of_attribute
        form.type_of_emotions.data = previous_codes.type_of_emotions
        form.type_of_subject.data = previous_codes.type_of_subject
        form.text_existence.data = previous_codes.text_existence
        form.type_of_audience.data = previous_codes.type_of_audience
        session['previous_steps'] += 1

    post_dir = post.local_download_directory
    video_files = glob.glob(os.path.join(post_dir, '*.mp4'))
    image_files = glob.glob(os.path.join(post_dir, '*.jpg')) + glob.glob(os.path.join(post_dir, '*.png'))
    media_file = None
    media_type = None
    if video_files:
        media_file = video_files[0]
        media_type = 'video'
    elif image_files:
        media_file = image_files[0]
        media_type = 'image'

    media_file = media_file.split('\\')
    media_file = media_file[8::]
    media_file = str('assets/img/' + '/'.join(media_file))
    form.post_id.data = post.id

    likes = shorten_number(post.likes)
    followers = shorten_number(db.session.query(Profiles.followers).filter(Profiles.id == post.profile_id).scalar())
    caption = re.sub(r'(\r\n){2,}','\r\n', str(post.caption).strip())

    return render_template('dashboard.html', post=post, caption = caption, followers=followers, likes=likes, form=form, media_file=media_file, media_type=media_type)

@app.route('/logout')
def logout():
    session['previous_steps'] = 0
    logout_user()
    return redirect(url_for('login'))

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)
 