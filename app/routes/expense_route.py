from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.expense import Expense
from datetime import datetime
from sqlalchemy import func
from sqlalchemy import func
from app.models.category import Category

expense_bp = Blueprint("expense", __name__)

@expense_bp.route("/expenses", methods=["POST"])
@jwt_required()
def add_expense():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    amount = data.get("amount")
    description = data.get("description")
    expense_date = data.get("expense_date")
    category_id = data.get("category_id")
    
    if not amount or not expense_date:
        return jsonify({"message": "Amount and date are required"}), 400

    expense = Expense(
        user_id=user_id,
        category_id=category_id,
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

@expense_bp.route("/expenses/<int:expense_id>", methods=["PUT"])
@jwt_required()
def update_expense(expense_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    expense = Expense.query.filter_by(
        id=expense_id,
        user_id=user_id
    ).first()

    if not expense:
        return jsonify({"message": "Expense not found"}), 404

    expense.amount = data.get("amount", expense.amount)
    expense.description = data.get("description", expense.description)

    if data.get("expense_date"):
        expense.expense_date = datetime.strptime(
            data.get("expense_date"), "%Y-%m-%d"
        )

    db.session.commit()

    return jsonify({"message": "Expense updated successfully"}), 200

@expense_bp.route("/expenses/<int:expense_id>", methods=["DELETE"])
@jwt_required()
def delete_expense(expense_id):
    user_id = get_jwt_identity()

    expense = Expense.query.filter_by(
        id=expense_id,
        user_id=user_id
    ).first()

    if not expense:
        return jsonify({"message": "Expense not found"}), 404

    db.session.delete(expense)
    db.session.commit()

    return jsonify({"message": "Expense deleted successfully"}), 200

@expense_bp.route("/expenses/summary/monthly", methods=["GET"])
@jwt_required()
def monthly_summary():
    user_id = get_jwt_identity()

    result = db.session.query(
        func.strftime('%Y-%m', Expense.expense_date),
        func.sum(Expense.amount)
    ).filter(
        Expense.user_id == user_id
    ).group_by(
        func.strftime('%Y-%m', Expense.expense_date)
    ).all()

    summary = []
    for month, total in result:
        summary.append({
            "month": month,
            "total_spent": float(total)
        })

    return jsonify(summary), 200

@expense_bp.route("/expenses/summary/category", methods=["GET"])
@jwt_required()
def category_summary():
    user_id = get_jwt_identity()

    result = db.session.query(
        Category.name,
        func.sum(Expense.amount)
    ).join(
        Expense, Expense.category_id == Category.id
    ).filter(
        Expense.user_id == user_id
    ).group_by(
        Category.name
    ).all()

    summary = []
    for category, total in result:
        summary.append({
            "category": category,
            "total_spent": float(total)
        })

    return jsonify(summary), 200
