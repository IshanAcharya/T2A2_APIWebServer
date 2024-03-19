from src.models import db
from marshmallow import Schema, fields

class Alert(db.Model):
    # Define table name for the model
    __tablename__ = 'alert'

    # Define columns for the model
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    day_of_week = db.Column(db.String(20), nullable=False)

    # Define relationship with other models
    user = db.relationship('User', backref='alert', lazy=True)
    product = db.relationship('Product', backref='alert', lazy=True)

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