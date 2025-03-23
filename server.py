from flask import Flask, jsonify, render_template, url_for, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
import requests, os
from dotenv import load_dotenv 
from forms import RegistrationForm, LoginForm 
from datetime import datetime, timezone
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Sequence, create_engine
from query import get_monthly_income
from models import db, User, Transaction, Savings  # Import from models.py

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('secret_cookie_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To avoid warnings
db.init_app(app)  # Initialize SQLAlchemy

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    user = User.query.first()

    # Get the current month and year
    selected_month = datetime.now().month
    selected_year = datetime.now().year

    # Call the function to get total_income and total_expenses
    total_income, total_expenses = get_monthly_income(user, selected_month, selected_year)

    # Pass the values to the template
    return render_template('dashboard.html', total_income=total_income, total_expenses=total_expenses)

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
        