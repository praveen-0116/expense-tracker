from flask import Flask
from .config import Config
from .extensions import db, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)


    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")


    from app.routes.expense_routes import expense_bp
    app.register_blueprint(expense_bp)


    from app.routes.category_routes import category_bp
    app.register_blueprint(category_bp)

    from app.routes.budget_routes import budget_bp
    app.register_blueprint(budget_bp)
    
      with app.app_context():
          db.create_all()

    return app
