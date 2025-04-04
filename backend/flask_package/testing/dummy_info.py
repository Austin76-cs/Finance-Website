#just for testing
from models.models import User, Transaction
from datetime import datetime
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
#