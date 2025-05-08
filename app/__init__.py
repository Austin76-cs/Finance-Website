import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    print('--- Flask app created ---')
    
    # Configure the app
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Plaid config
    app.config['PLAID_ENVIRONMENT'] = os.getenv('PLAID_ENVIRONMENT')
    app.config['PLAID_CLIENT_ID'] = os.getenv('PLAID_CLIENT_ID')
    app.config['PLAID_SECRET'] = os.getenv('PLAID_SECRET')
    
    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Register blueprints
    from app.routes.auth import auth
    from app.routes.main import main
    from app.routes.plaid import plaid_bp
    
    app.register_blueprint(auth)
    print('Registered blueprint: auth')
    app.register_blueprint(main)
    print('Registered blueprint: main')
    app.register_blueprint(plaid_bp)
    print('Registered blueprint: plaid_bp')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    print('--- URL MAP ---')
    print(app.url_map)
    
    return app 