from src.models import db

class Purchase(db.model):
    __tablename__ = 'purchase'

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