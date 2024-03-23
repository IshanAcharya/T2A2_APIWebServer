from src import db
from marshmallow import Schema, fields

class Product(db.Model):
    # Define table name for the model
    __tablename__ = 'products'

    # Define columns for the model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100))
    category = db.Column(db.String(100))

    # Define relationships with other models
    purchases = db.relationship('Purchase', backref='product', lazy=True)
    alerts = db.relationship('Alert', backref='product', lazy=True)
    promotions = db.relationship('Promotion', backref='product', lazy=True)

    def serialise(self):
        return{
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'category': self.category
        }
    
    # Ensure product names are unique
    __table_args__ = (db.UniqueConstraint('name', 'brand', 'category', name='unique_product'),)
    
class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    brand = fields.Str(required=True)
    category = fields.Str(required=True)

product_schema = ProductSchema()