from src import db
from marshmallow import Schema, fields

class Alert(db.Model):
    # Define table name for the model
    __tablename__ = 'alerts'

    # Define columns for the model
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    day_of_week = db.Column(db.String(20), nullable=False)

    # Define relationship with other models
    users = db.relationship('User', backref='alert', lazy=True)
    products = db.relationship('Product', backref='alert', lazy=True)

    def serialise(self):
        return{
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'day_of_week': self.day_of_week
        }
    
class AlertSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    product_id = fields.Int(required=True)
    day_of_week = fields.Str(required=True)