import os
from flask import Flask
from marshmallow.exceptions import ValidationError
from dotenv import load_dotenv
from src import db
from src import ma
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():    
    # Create Flask application instance
    app = Flask(__name__)
    
    # Ensure JSON responses are not sorted for consistency
    app.json.sort_keys = False
    
    # Load environment variables from .env
    load_dotenv()

    # Configure Flask app with environment variables

    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DATABASE_URI")
    app.config["JWT_SECRET_KEY"]=os.environ.get("JWT_SECRET_KEY")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 60 * 60 * 24  # Access token expires in 1 day
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 60 * 60 * 24 * 30 # Refresh token expires in 30 days
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies'] # Identifies where JWT tokens are located

    # Connect libraries from init.py with flask app

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Global error handling for entire application

    # Error handler for Bad Request (400)
    @app.errorhandler(400)
    def bad_request(error):
        return{"error": str(error)}, 400
    
    # Error handler for Not Found (404)
    @app.errorhandler(404)
    def not_found(error):
        return{"error": str(error)}, 404
    
    # Error handler for Internal Server Error (500)
    @app.errorhandler(500)
    def internal_server_error(error):
        return{"error": str(error)}, 500
    
    # Error handler for Marshmallow Validation Error
    @app.errorhandler(ValidationError)
    def validation_error(error):
        return{"error": error.messages}, 400

    # Register Blueprint controllers

    # Register database command controller
    from src.controllers.cli_controller import db_commands

    app.register_blueprint(db_commands)

    # Register authentication controller
    from src.controllers.auth_controller import auth_bp

    app.register_blueprint(auth_bp)

    # Register user controller
    from src.controllers.user_controller import user_bp 

    app.register_blueprint(user_bp)

    # Register purchase controller
    from src.controllers.purchase_controller import purchase_bp

    app.register_blueprint(purchase_bp)

    # Register product controller
    from src.controllers.product_controller import product_bp

    app.register_blueprint(product_bp)

    # Register promotion controller
    from src.controllers.promotion_controller import promotion_bp

    app.register_blueprint(promotion_bp)

    # Register store controller
    from src.controllers.store_controller import store_bp

    app.register_blueprint(store_bp, url_prefix='/store')

    # Register alert controller
    from src.controllers.alert_controller import alert_bp

    app.register_blueprint(alert_bp)

    return app