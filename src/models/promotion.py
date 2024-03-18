from src.models import db

class Promotion(db.Model):
    __tablename__ = 'promotion'

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