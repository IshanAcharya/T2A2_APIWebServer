from src import db
from marshmallow import Schema, fields

class Product(db.Model):
    # Define table name for the model
    __tablename__ = 'products'

    # Define columns for the model
    id = db.Column(db.Integer, primary_key=True) # Primary Key for the product
    name = db.Column(db.String(100), nullable=False) # Name of the product
    brand = db.Column(db.String(100)), # Brand of the product
    category = db.Column(db.String(100)) # Category of the product

    # Define relationships with other models
    purchases = db.relationship('Purchase', backref='product', lazy=True) # Relationship with the Purchase model, linking products to their purchases 
    alerts = db.relationship('Alert', backref='product', lazy=True) # Relationship with the Alert model, linking products to their alerts
    promotions = db.relationship('Promotion', backref='product', lazy=True) # Relationship with the Promotion model, linking products to their promotions

    # Method to serialize Product object
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'category': self.category
        }

# Schema for serialization/deserialization of Product objects   
class ProductSchema(Schema):
    id = fields.Int(dump_only=True) # ID field is read only
    name = fields.Str(required=True) # Product name is required
    brand = fields.Str(required=True) # Product brand is required
    category = fields.Str(required=True) # Product category is required

# Schema for serialization/deserialization of Product objects
product_schema = ProductSchema()