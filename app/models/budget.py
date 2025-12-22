from app.extensions import db
from datetime import datetime

class Budget(db.Model):
    __tablename__ = "budgets"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    monthly_limit = db.Column(db.Numeric(10, 2), nullable=False)
    month_year = db.Column(db.String(7), nullable=False)  # YYYY-MM
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
