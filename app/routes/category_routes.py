from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.category import Category

category_bp = Blueprint("category", __name__)

@category_bp.route("/categories", methods=["POST"])
@jwt_required()
def add_category():
    user_id = get_jwt_identity()
    data = request.get_json()

    name = data.get("name")

    if not name:
        return jsonify({"message": "Category name required"}), 400

    category = Category(name=name, user_id=user_id)
    db.session.add(category)
    db.session.commit()

    return jsonify({"message": "Category added"}), 201


@category_bp.route("/categories", methods=["GET"])
@jwt_required()
def get_categories():
    user_id = get_jwt_identity()

    categories = Category.query.filter_by(user_id=user_id).all()

    result = [{"id": c.id, "name": c.name} for c in categories]
    return jsonify(result), 200
