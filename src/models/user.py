from src import db
from marshmallow import Schema, fields, validates, ValidationError

class User(db.Model):
    # Define table name for the model
    __tablename__ = 'users'

    # Define columns for the model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=True, nullable=False)


# Define relationships with other models
    purchases = db.relationship('Purchase', backref='buyer', lazy=True)
    alerts = db.relationship('Alert', backref='owner', lazy=True)


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)

    @validates('password')
    def validate_password(self, value):
        if len(value) <8:
            raise ValidationError('Password must be at least 8 characters long.')
        

user_schema = UserSchema()