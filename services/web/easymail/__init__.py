from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_mail import Mail



import os


app = Flask(__name__)
app.config.from_object("easymail.config.Config")





db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'NewUsers.login'
mail.init_app(app)

from easymail.Main.routes import Main
from easymail.NewUsers.routes import NewUsers
from easymail.Panel.routes import Panel


app.register_blueprint(Main)
app.register_blueprint(NewUsers)
app.register_blueprint(Panel)
