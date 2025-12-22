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


    @expense_bp.route("/expenses", methods=["GET"])
    @jwt_required()
    def get_expenses():
        user_id = get_jwt_identity()
        
        expenses = Expense.query.filter_by(user_id=user_id).order_by(
            Expense.expense_date.desc()
        ).all()
        
        result = []
        for expense in expenses:
            result.append({
                "id": expense.id,
                "amount": float(expense.amount),
                "description": expense.description,
                "expense_date": expense.expense_date.strftime("%Y-%m-%d"),
                "created_at": expense.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
            
            return jsonify(result), 200
