from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from app.extensions import db
from app.models.budget import Budget
from app.models.expense import Expense

budget_bp = Blueprint("budget", __name__)

@budget_bp.route("/budgets", methods=["POST"])
@jwt_required()
def set_budget():
    user_id = get_jwt_identity()
    data = request.get_json()

    category_id = data.get("category_id")
    monthly_limit = data.get("monthly_limit")
    month_year = data.get("month_year")

    if not category_id or not monthly_limit or not month_year:
        return jsonify({"message": "All fields required"}), 400

    budget = Budget(
        user_id=user_id,
        category_id=category_id,
        monthly_limit=monthly_limit,
        month_year=month_year
    )

    db.session.add(budget)
    db.session.commit()

    return jsonify({"message": "Budget set successfully"}), 201


@budget_bp.route("/budgets/check", methods=["GET"])
@jwt_required()
def check_budget():
    user_id = get_jwt_identity()
    category_id = request.args.get("category_id")
    month_year = request.args.get("month_year")

    budget = Budget.query.filter_by(
        user_id=user_id,
        category_id=category_id,
        month_year=month_year
    ).first()

    if not budget:
        return jsonify({"message": "No budget set"}), 404

    total_spent = db.session.query(
        func.sum(Expense.amount)
    ).filter(
        Expense.user_id == user_id,
        Expense.category_id == category_id,
        func.strftime('%Y-%m', Expense.expense_date) == month_year
    ).scalar() or 0

    return jsonify({
        "monthly_limit": float(budget.monthly_limit),
        "spent": float(total_spent),
        "remaining": float(budget.monthly_limit - total_spent)
    }), 200
