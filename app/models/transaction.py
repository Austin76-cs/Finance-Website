from datetime import datetime
from app import db

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(100), nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    plaid_transaction_id = db.Column(db.String(100), unique=True, nullable=True)
    
    def __repr__(self):
        return f"Transaction('{self.description}', '{self.amount}', '{self.date}')" 