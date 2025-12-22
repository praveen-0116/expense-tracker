from app.extensions import db
from datetime import datetime

class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    category_id = db.Column(
        db.Integer, 
        db.ForeignKey("categories.id"),
        nullable=True
    )
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(255))
    expense_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
