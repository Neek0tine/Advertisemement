from flask_login import UserMixin
from . import db

class Coder(UserMixin, db.Model):
    __tablename__ = 'coder'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), nullable=False, unique=True)

class Codes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('coder.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    number_of_memes = db.Column(db.Integer, nullable=False)
    type_of_memes = db.Column(db.Integer, nullable=False)
    type_of_movement = db.Column(db.Integer, nullable=False)
    type_of_emotions = db.Column(db.Integer, nullable=False)
    type_of_subject = db.Column(db.Integer, nullable=False)

class Profiles(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=True)
    profile_pic_url = db.Column(db.String(255), nullable=True)
    followers = db.Column(db.Integer, nullable=True)
    following = db.Column(db.Integer, nullable=True)
    bio = db.Column(db.Text, nullable=True)

class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    post_url = db.Column(db.String(255), nullable=True)
    caption = db.Column(db.Text, nullable=True)
    likes = db.Column(db.Integer, nullable=True)
    date_posted = db.Column(db.DateTime, nullable=True)
    engagement = db.Column(db.Float, nullable=True)
    local_download_directory = db.Column(db.String(255), nullable=True)

    profile = db.relationship('Profiles', backref=db.backref('posts', lazy=True))