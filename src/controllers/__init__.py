from flask import Blueprint

# Blueprints for each controllers

user_bp = Blueprint ('user', __name__)
product_bp = Blueprint ('product', __name__)
promotion_bp = Blueprint ('promotion', __name__)
purchase_bp = Blueprint ('purchase', __name__)
store_bp = Blueprint ('store', __name__)
alert_bp = Blueprint ('alert', __name__)