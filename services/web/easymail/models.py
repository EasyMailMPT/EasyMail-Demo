from datetime import datetime
import string
from random import choices
from easymail import db ,login_manager,app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    phone = db.Column(db.String(255), unique=False, nullable=True)
    email = db.Column(db.String(255),unique=True,nullable=False)
    password = db.Column(db.String(255),unique=False,nullable=False)
    role = db.Column(db.String(60),unique=False,nullable=False,server_default='free')
    confirmed = db.Column(db.Boolean, nullable=False, server_default='False')
    confirmed_on = db.Column(db.DateTime, nullable=True,server_default=db.func.now(), server_onupdate=db.func.now())
    deleted = db.Column(db.Boolean, nullable=False, server_default='False')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    userEmails = db.relationship('Websites',backref="websites",lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

class Websites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(40000), unique=False, nullable=False)
    keyword = db.Column(db.String(4000), unique=False, nullable=False)
    deleted = db.Column(db.Boolean, nullable=False, server_default='False')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    emails = db.relationship('Emails', backref='websites',lazy=True)

class Emails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=False)
    website_id = db.Column(db.Integer, db.ForeignKey('websites.id'), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
db.create_all()