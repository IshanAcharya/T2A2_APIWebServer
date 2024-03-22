from src import db
from marshmallow import Schema, fields

class Promotion(db.Model):
    # Define table name for the model
    __tablename__ = 'promotions'

    # Define columns for the model
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchases.id'))
    promotion_type = db.Column(db.String(50), nullable=False)
    promotion_discount = db.Column(db.Float, nullable=False)

    # Define relationship with other models
    purchases = db.relationship('Purchase', backref='promotions')

    def serialise(self):
        return{
            'id': self.id,
            'product_id': self.product_id,
            'promotion_type': self.promotion_type,
            'promotion_discount': self.promotion_discount
        }
    
class PromotionSchema(Schema):
    id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True)
    promotion_type = fields.Str(required=True)
    promotion_discount = fields.Float(required=True)

promotion_schema = PromotionSchema()