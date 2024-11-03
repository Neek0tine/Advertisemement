import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_session import Session
from .config import Config

template_dir = os.path.abspath('frontend/templates')
static_dir = os.path.abspath('frontend/templates/assets')
serve_folder = 'frontend/templates/scraps'

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config.from_object(Config)
app.config['SESSION_TYPE'] = 'filesystem'


db = SQLAlchemy(app)
csrf = CSRFProtect(app) 
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
Session(app)  # Enable session management

@login_manager.user_loader
def load_user(user_id):
    from .dbmodel import Coder
    return Coder.query.get(int(user_id))

from .routes import *

app.app_context().push()
