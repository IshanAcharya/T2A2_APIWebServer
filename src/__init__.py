from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy () # Initialise SQLAlchemy for database management
ma = Marshmallow () # Initialise Marshmallow for serialization and deserialization
bcrypt = Bcrypt () # Initialise Bcrypt for password hashing and verification
jwt = JWTManager() # Initialise JWTManager for JSON Web Token handling