from src import db
from marshmallow import Schema, fields

class Promotion(db.Model):
    # Define table name for the model
    __tablename__ = 'promotions'

    # Define columns for the model
    id = db.Column(db.Integer, primary_key=True) # Primary Key for the promotion
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchases.id')) # Foreign Key referencing the Purchase table
    promotion_type = db.Column(db.String(50), nullable=False) # Type of promotion
    promotion_discount = db.Column(db.Float, nullable=False) # Discount value of the promotion

    # Define relationship with other models
    purchases = db.relationship('Purchase', backref='promotions') # Relationship with the Purchase model, linking promotions to their purchases

    # Method to serialize Purchase object
    def serialize(self):
        return{
            'id': self.id,
            'product_id': self.product_id,
            'promotion_type': self.promotion_type,
            'promotion_discount': self.promotion_discount
        }

# Schema for serialization/deserialization of Promotion objects
class PromotionSchema(Schema):
    id = fields.Int(dump_only=True) # ID field is read only
    product_id = fields.Int(required=True) # Product ID is required
    promotion_type = fields.Str(required=True) # Promotion type is required
    promotion_discount = fields.Float(required=True) # Promotion discount is required

# Schema for serialization/deserialization of Promotion objects
promotion_schema = PromotionSchema()