from datetime import datetime
from flask_package import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
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

class Savings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))