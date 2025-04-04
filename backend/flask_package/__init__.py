import os
from dotenv import load_dotenv 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flaskapp = Flask(__name__, 
           template_folder='../frontend/templates',
           static_folder='../frontend/static')
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('secret_cookie_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Database file
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

with app.app_context():
    db.drop_all() 
    db.create_all()
    db.session.commit()
