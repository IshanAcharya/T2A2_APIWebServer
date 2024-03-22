from src import db
from marshmallow import Schema, fields

class Store(db.Model):
    # Define table name for the model
    __tablename__ = 'stores'

    # Define columns for the model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200), nullable=False)

    # Define relationship with other models
    purchase = db.relationship('Purchase', backref='stores', lazy=True)

    def serialise(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'location': self.location
        }
    

class StoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    type = fields.Str(required=True)
    location = fields.Str(required=True)


store_schema = StoreSchema()