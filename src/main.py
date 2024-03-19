from flask import Flask
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from marshmallow.exceptions import ValidationError
from dotenv import load_dotenv
from init import db, ma, bcrypt, jwt
import os

def create_app():    
    app = Flask(__name__)
    app.json.sort_keys = False
    
    # Load environment variables from .env
    from dotenv import load_dotenv

    load_dotenv()

    # Configurations

    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DATABASE_URI")
    app.config["JWT_SECRET_KEY"]=os.environ.get("JWT_SECRET_KEY")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 60 * 60 * 24  # Access token expires in 1 day
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 60 * 60 * 24 * 30 # Refresh token expires in 30 days
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies'] # Identifies where JWT tokens are located

    # Connect libraries with flask app

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register Blueprint controllers

    from controllers.cli_controller import cli_bp

    app.register_blueprint(user_bp)

    from controllers.user_controller import user_bp 

    app.register_blueprint(user_bp)

    from controllers.purchase_controller import purchase_bp

    app.register_blueprint(purchase_bp)

    from controllers.product_controller import product_bp

    app.register_blueprint(product_bp)

    from controllers.promotion_controller import promotion_bp

    app.register_blueprint(promotion_bp)

    from controllers.store_controller import store_bp

    app.register_blueprint(store_bp)

    from controllers.alert_controller import alert_bp

    app.register_blueprint(alert_bp)

    return app

# Define route for authentication
@app.route('/protected')
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200