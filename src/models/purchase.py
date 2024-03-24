from src import db
from marshmallow import Schema, fields

class Purchase(db.Model):
    # Define table name for the model
    __tablename__ = 'purchases'

    # Define columns for the model
    id = db.Column(db.Integer, primary_key=True) # Primary Key for the purchase
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Foreign Key referencing User table
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False) # Foreign Key referencing Product table
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False) # Foreign Key referencing Store table
    promotion_id = db.Column(db.Integer, db.ForeignKey('promotions.id')) # Foreign Key referencing Promotion table
    price = db.Column(db.Float, nullable=False) # Price of the purchase
    purchase_date = db.Column(db.DateTime, nullable=False) # Time and date of the purchase

    # Define relationship with other models
    users = db.relationship('User', backref='purchases') # Relationship with User model, linking purchases to users
    products = db.relationship('Product', backref='purchases') # Relationship with Product model, linking purchases to products
    stores = db.relationship('Store', backref='purchases') # Relationship with Store Model, linking purchases to stores
    promotions = db.relationship('Promotion', backref='purchases') # Relatonship with Promotion model, linking purchases to promotions

    # Method to serialize Purchase object
    def serialize(self):
        return{
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'store_id': self.store_id,
            'promotion_id': self.promotion_id,
            'price': self.price,
            'purchase_date': self.purchase_date.strftime('%D-%m-%y %H:%M:%S')
        }

# Schema for serialization/deserialization of Purchase objects
class PurchaseSchema(Schema):
    id = fields.Int(dump_only=True) # ID field is read only
    user_id = fields.Int(required=True) # User ID is required
    product_id = fields.Int(required=True) # Product ID is required
    store_id = fields.Int(required=True) # Store ID is required
    promotion_id = fields.Int() # Promotion ID is optional
    price = fields.Float(required=True) # Price is required
    purchase_date = fields.DateTime(required=True) # Purchase date is required

# Schema for serialization/deserialization of Purchase objects
purchase_schema = PurchaseSchema()