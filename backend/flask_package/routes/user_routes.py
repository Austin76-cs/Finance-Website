from flask import render_template, url_for, flash, redirect, request
from backend import app, db, bcrypt
from auth.forms import RegistrationForm, LoginForm
from backend.flask_package.models import User, Transaction, Savings
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from db.query import get_monthly_income

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('frontend/templates/register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)
