from datetime import datetime
from sqlalchemy import func
import calendar
from server import User, Transaction, Savings

def get_monthly_income(user, selected_month, selected_year):
    # Querys transactions for the selected month and year
    first_day, last_day = calendar.monthrange(selected_year, selected_month)
    start_of_month = datetime(selected_year, selected_month, 1)
    end_of_month = datetime(selected_year, selected_month, last_day, 23, 59, 59) 
    monthly_transactions = Transaction.query.filter(Transaction.user_id == user.id,
                                                    Transaction.date >= start_of_month,
                                                    Transaction.date <= end_of_month,
     ).all()
    
    total_income = sum(t.amount for t in monthly_transactions if t.amount > 0)
    total_expenses = sum(t.amount for t in monthly_transactions if t.amount < 0)

    return total_income, total_expenses