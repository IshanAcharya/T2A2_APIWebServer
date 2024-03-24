from src import db
from marshmallow import Schema, fields

class Alert(db.Model):
    # Define table name for the model
    __tablename__ = 'alerts'

    # Define columns for the model
    id = db.Column(db.Integer, primary_key=True) # Primary Key for the alert
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Foreign Key referencing User table
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False) # Foreign Key referencing Product table
    day_of_week = db.Column(db.String(20), nullable=False) # Day of the week for the alert

    # Define relationship with other models
    users = db.relationship('User', backref='alert', lazy=True) # Relationship with the User model, linking alerts to their users
    products = db.relationship('Product', backref='alert', lazy=True) # Relationship with the Product model, linking alerts to their products

    # Method to serialize Alert object
    def serialize(self):
        return{
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'day_of_week': self.day_of_week
        }

# Schema for serialization/deserialization of Alert objects
class AlertSchema(Schema):
    id = fields.Int(dump_only=True) # ID is read only
    user_id = fields.Int(required=True) # User ID is required
    product_id = fields.Int(required=True) # Product ID is required
    day_of_week = fields.Str(required=True) # Day of week is required

# Schema for serialization/deserialization of Alert objects
alert_schema = AlertSchema()