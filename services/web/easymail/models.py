from datetime import datetime
import string
from random import choices
from easymail import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    phone = db.Column(db.String(255), unique=False, nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String(60), unique=False, nullable=False, server_default='free')
    confirmed = db.Column(db.Boolean, nullable=False, server_default='False')
    confirmed_on = db.Column(db.DateTime, nullable=True, server_default=db.func.now(), server_onupdate=db.func.now())
    deleted = db.Column(db.Boolean, nullable=False, server_default='False')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

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

class Keywords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(4000), unique=False, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    last_searched = db.Column(db.DateTime, server_default=db.func.now())

    emails = db.relationship('Emails', backref='websites', lazy=True)


class Emails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=False)
    website = db.Column(db.String(40000), unique=False, nullable=False)

    keyword_id = db.Column(db.Integer, db.ForeignKey('keywords.id'), nullable=True)


db.create_all()


def get_user_by_email(email):
    query = db.select(User).where(User.name == email)
    return db.session.execute(query)


def get_emails_from_keyword(keyword, session = db.session):
    """returns dictionary with urls as keys and list of emails as values"""
    result = []
    q = db.select(Emails).where(Keywords.keyword == keyword).where(Emails.keyword_id == Keywords.id).execution_options(synchronize_session="fetch")
    emails = session.execute(q)
    for email in emails:
        result.append({'url': email.Emails.website, 'email': email.Emails.email})
    return result

def check_if_keyword_in_database(keyword, count = 1, session=db.session):
    result = session.query(Emails).filter(Keywords.keyword==keyword, Keywords.id == Emails.keyword_id).count()
    if result >= count:
        print('True')
        return True
    else:
        print('True')
        return False

def delete_results_of_keyword(keyword, session = db.session):
    q = db.delete(Emails).where(Keywords.keyword == keyword).where(Emails.keyword_id == Keywords.id).execution_options(synchronize_session="fetch")
    session.execute(q)
    q = db.delete(Keywords).where(Keywords.keyword == keyword)
    session.execute(q)