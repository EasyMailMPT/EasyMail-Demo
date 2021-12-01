import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SEND_FILE_MAX_AGE_DEFAULT = 0
    
    SECRET_KEY=os.getenv("SECRET_KEY")
    SECURITY_PASSWORD_SALT=os.getenv("SECURITY_PASSWORD_SALT")
    
    SERP_KEY=os.getenv("SERP_KEY")

    STATIC_FOLDER = f"{os.getenv('APP_FOLDER')}/easymail/static"