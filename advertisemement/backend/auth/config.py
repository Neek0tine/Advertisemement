import secrets

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://neeko:rosebud@localhost/advertisemement'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_hex()
    
