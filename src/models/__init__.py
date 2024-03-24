from flask_sqlalchemy import SQLAlchemy

# Initialise SQLAlchemy
db = SQLAlchemy()

# Import models
from .user import User # Import User model
from .product import Product # Import Product model
from .promotion import Promotion # Import Promotion model
from .purchase import Purchase # Import Purchase model
from .store import Store # Import Store model
from .alert import Alert # Import Alert model