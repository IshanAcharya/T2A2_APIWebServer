from flask import Blueprint

# Define Blueprints for each controllers

user_bp = Blueprint ('user', __name__) # Blueprint for user controller
product_bp = Blueprint ('product', __name__) # Blueprint for product controller
promotion_bp = Blueprint ('promotion', __name__) # Blueprint for promotion controller
purchase_bp = Blueprint ('purchase', __name__) # Blueprint for purchase controller
store_bp = Blueprint ('store', __name__) # Blueprint for store controller
alert_bp = Blueprint ('alert', __name__) # Blueprint for alert controller
auth_bp = Blueprint ('auth', __name__) # Blueprint for authentication controller
db_commands = Blueprint ('db', __name__) # Blueprint for database command controller