import email
import bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

#app initialization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:fuzzbutt@localhost/do_it_already'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'log_in'
login_manager.login_message_category = 'info'
#email setup for password reset
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('AdminEmail')
app.config['MAIL_PASSWORD'] = os.environ.get('AdminEmailPass')
mail = Mail(app)

app.config['SECRET_KEY'] = 'secretkeyhassecrets'

from ToDoListApp import routes