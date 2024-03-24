from src import db
from marshmallow import Schema, fields, validates, ValidationError

class User(db.Model):
    # Define table name for the model
    __tablename__ = 'users'

    # Define columns for the model
    id = db.Column(db.Integer, primary_key=True) # Primary Key for the user
    username = db.Column(db.String(50), unique=True, nullable=False) # Username of the user
    email = db.Column(db.String(120), unique=True, nullable=False) # Email address of the user
    password = db.Column(db.String(60), unique=True, nullable=False) # Password of the user

# Define relationships with other models
    purchases = db.relationship('Purchase', backref='buyer', lazy=True) # Relationship with the Purchase model, linking users to their purchases
    alerts = db.relationship('Alert', backref='owner', lazy=True) # Relationship with the Alert model, linking users to their alerts

# Schema for serialization/deserialization of User objects
class UserSchema(Schema):
    id = fields.Integer(dump_only=True) # ID field is read only
    username = fields.String(required=True) # Username is required
    email = fields.Email(required=True) # Email is required and must be valid
    password = fields.String(required=True, load_only=True) # Password is required and only loaded and not dumped

    @validates('password')
    def validate_password(self, value):
        # Validation for password length
        if len(value) <8:
            raise ValidationError('Password must be at least 8 characters long.')
        
# Schema for serialization/deserialization of User objects
user_schema = UserSchema()