import glob
import re
import os, sys
from . import app, db
from .dbmodel import Coder, Codes, Posts, Profiles
from flask import render_template, redirect, url_for, flash, session, send_from_directory
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, RadioField
from wtforms.validators import InputRequired, DataRequired


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
    if form.validate_on_submit():
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
        print('[+] CODES VALIDATED ') 
        db.session.add(categorized_post)
        db.session.commit()

        flash('Post categorized successfully', 'success')

        # After submission, clear the current post ID to fetch a new random post
        session.pop('current_post_id', None)
        return redirect(url_for('dashboard'))

    # Retrieve the current post ID from the session, if available
    current_post_id = session.get('current_post_id')
    if not current_post_id:
        # If no current post ID in session, fetch a new random post
        post = Posts.query.order_by(db.func.rand()).first()
        session['current_post_id'] = post.id
    else:
        # Otherwise, retrieve the post from the database using the session-stored ID
        post = Posts.query.get(current_post_id)

    # Check for video and image files in the post's directory
    post_dir = post.local_download_directory
    

    video_files = glob.glob(os.path.join(post_dir, '*.mp4'))
    image_files = glob.glob(os.path.join(post_dir, '*.jpg')) + glob.glob(os.path.join(post_dir, '*.png'))

    # Prioritize video over image
    media_file = None
    media_type = None
    if video_files:
        media_file = video_files[0]
        media_type = 'video'
    elif image_files:
        media_file = image_files[0]
        media_type = 'image'

    likes = post.likes
    followers = db.session.query(Profiles.followers).filter(Profiles.id == post.profile_id).scalar()

    def shorten_number(number_to_shorten):
        from numerize import numerize 
        return str(numerize.numerize(number_to_shorten))

    likes = shorten_number(likes)
    followers = shorten_number(followers)

    media_file = media_file.split('\\')
    media_file = media_file[8::]
    media_file = str('assets/img/' + '/'.join(media_file))
    form.post_id.data = post.id


    caption = str(post.caption).strip()
    # caption = ''.join(caption.splitlines())
    caption = re.sub(r'(\r\n){2,}','\r\n', caption)
    return render_template('dashboard.html', post=post, caption = caption, followers=followers, likes=likes, form=form, media_file=media_file, media_type=media_type)

@app.route('/previous', methods=['GET', 'POST'])
@login_required
def previous():
    form = CategorizationForm()
    previous_post = Codes.query.filter_by(user_id=current_user.id).order_by(Codes.id.desc()).first()
    session['current_post_id'] = previous_post.post_id
    form.post_id.data = previous_post.post_id
    form.number_of_panels.data = previous_post.number_of_panels
    form.type_of_image.data = previous_post.type_of_image
    form.type_of_movement.data = previous_post.type_of_movement
    form.type_of_attribute.data = previous_post.type_of_attribute
    form.type_of_emotions.data = previous_post.type_of_emotions
    form.type_of_subject.data = previous_post.type_of_subject
    form.text_existence.data = previous_post.text_existence
    form.type_of_audience.data = previous_post.type_of_audience
    print(form.data, file=sys.stderr)
    return redirect(url_for('dashboard'))

@app.route('/next', methods=['GET', 'POST'])
@login_required
def next():
    # Logic for handling next post action
    session.pop('current_post_id', None)
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)
 