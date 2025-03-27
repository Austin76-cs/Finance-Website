from flask import Flask, jsonify, render_template, url_for, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
import requests, os
from dotenv import load_dotenv 
from forms import RegistrationForm, LoginForm 
from datetime import datetime, timezone
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Sequence, create_engine
from query import get_monthly_income
from models import db, User, Transaction, Savings 
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('secret_cookie_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To avoid warnings
db.init_app(app)  # Initialize SQLAlchemy
bcrypt = Bcrypt(app)

test_user = [User(id = 1, email = "test_email.com", password = 'password', )]

test_transactions = [
            Transaction(
                user_id=1,
                amount=100.00,
                description="",
                date=datetime.now()
            ),
            Transaction(
                user_id=1,
                amount=-50.00,
                description="",
                date=datetime.now()
            )
        ]
with app.app_context():
    db.drop_all()  # Drops all tables
    db.create_all()
    db.session.add_all(test_user)
    db.session.add_all(test_transactions)
    db.session.commit()

@app.route('/')
def home():
    user = User.query.first()

    # Get the current month and year
    selected_month = datetime.now().month
    selected_year = datetime.now().year

    # Call the function to get total_income and total_expenses
    total_income, total_expenses = get_monthly_income(user, selected_month, selected_year)

    # Pass the values to the template
    return render_template('index.html', total_income=total_income, total_expenses=total_expenses)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.email.data}, you can now login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title= 'Register' ,form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('login.html', title = 'Login', form=form)

if __name__ == "__main__":
    app.run(debug=True)
        