# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initialize SQLAlchemy without binding it to an app

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

    '''@property
    def type(self):
        return 'income' if self.amount > 0 else 'expense'  '''
    '''def __repr__(self):models.py
        return f"Transaction(amount={self.amount}, type='{self.type}', date='{self.date}', description='{self.description}')" '''

class Savings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))