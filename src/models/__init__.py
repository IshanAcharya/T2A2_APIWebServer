from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .product import Product
from .promotion import Promotion
from .purchase import Purchase
from .store import Store
from .alert import Alert

