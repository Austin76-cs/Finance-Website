from flask import Flask, jsonify, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import requests, os
from dotenv import load_dotenv 
from forms import RegistrationForm, LoginForm 
from datetime import datetime, timezone
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Sequence, create_engine
import query

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('secret_cookie_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To avoid warnings
db = SQLAlchemy(app)  # Initialize SQLAlchemy

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    plaid_access_token = db.Column(db.String(200))
    #created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    def __repr__(self):
        return f"User(email='{self.email}', password='{self.password}')"

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)  # Positive for income, negative for expenses
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(200))  # Optional: e.g., "Salary", "Groceries"
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def type(self):
        return 'income' if self.amount > 0 else 'expense' 
    def __repr__(self):
        return f"Transaction(amount={self.amount}, type='{self.type}', date='{self.date}', description='{self.description}')"

class Savings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title= 'Register' ,form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('login.html', title = 'Login', form=form)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)

#with app.app_context():
    # Create a new user
    #user_1 = User(email="example@example.com", password="password")
    
    # Add the user to the database session
    #db.session.add(user_1)
    
    # Commit the session to save the user in the database
    #db.session.commit()

with app.app_context():
    User.query.all()
        