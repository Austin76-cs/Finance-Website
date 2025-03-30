import os
#from flaskwebsite.dotenv import load_dotenv 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
#load_dotenv()
secret_cookie_key = 'sjidnaoiudba8sgd'
app.config['SECRET_KEY'] = os.getenv('secret_cookie_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Database file
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

import routes