from src.models import db
from marshmallow import Schema, fields

class Promotion(db.Model):
    # Define table name for the model
    __tablename__ = 'promotion'

    # Define columns for the model
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'))
    promotion_type = db.Column(db.String(50), nullable=False)
    promotion_discount = db.Column(db.Float, nullable=False)

    # Define relationship with other models
    product = db.relationship('Product', backref='promotion')
    purchase = db.relationship('Purchase', backref='promotion')

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
