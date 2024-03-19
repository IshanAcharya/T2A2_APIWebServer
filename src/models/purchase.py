from src.models import db
from marshmallow import Schema, fields

class Purchase(db.model):
    # Define table name for the model
    __tablename__ = 'purchase'

    # Define columns for the model
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    promotion_id = db.Column(db.Integer, db.ForeignKey('promotion.id'))
    price = db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False)

    # Define relationship with other models
    user = db.relationship('User', backref='purchase')
    product = db.relationship('Product', backref='purchase')
    store = db.relationship('Store', backref='purchases')
    promotion = db.relationship('Promotion', backref='purchase')

    def serialise(self):
        return{
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'store_id': self.store_id,
            'promotion_id': self.promotion_id,
            'price': self.price,
            'purchase_date': self.purchase_date.strftime('%D-%m-%y %H:%M:%S')
        }
    
class PurchaseSchema(Schema):
    id = fields.int(dump_only=True)
    user_id = fields.Int(required=True)
    product_id = fields.Int(required=True)
    store_id = fields.Int(required=True)
    promotion_id = fields.Int()
    price = fields.Float(required=True)
    purchase_date = fields.DateTime(required=True)