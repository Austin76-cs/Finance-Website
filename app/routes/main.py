from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models import Transaction
from datetime import datetime
from sqlalchemy import extract

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main.route('/')
@main.route('/home')
@login_required
def home_old():
    # Get the current month's transactions
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    transactions = Transaction.query.filter(
        Transaction.user_id == current_user.id,
        extract('month', Transaction.date) == current_month,
        extract('year', Transaction.date) == current_year
    ).all()
    
    # Calculate totals
    total_income = sum(t.amount for t in transactions if t.amount > 0)
    total_expenses = sum(abs(t.amount) for t in transactions if t.amount < 0)
    
    return render_template('index.html', 
                         total_income=total_income,
                         total_expenses=total_expenses,
                         transactions=transactions) 