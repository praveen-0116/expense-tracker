from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.expense import Expense
from datetime import datetime

expense_bp = Blueprint("expense", __name__)

@expense_bp.route("/expenses", methods=["POST"])
@jwt_required()
def add_expense():
    data = request.get_json()
    user_id = get_jwt_identity()

    amount = data.get("amount")
    description = data.get("description")
    expense_date = data.get("expense_date")

    if not amount or not expense_date:
        return jsonify({"message": "Amount and date are required"}), 400

    expense = Expense(
        user_id=user_id,
        amount=amount,
        description=description,
        expense_date=datetime.strptime(expense_date, "%Y-%m-%d")
    )

    db.session.add(expense)
    db.session.commit()

    return jsonify({"message": "Expense added successfully"}), 201
