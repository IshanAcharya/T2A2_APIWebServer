from src import db
from marshmallow import Schema, fields

class Store(db.Model):
    # Define table name for the model
    __tablename__ = 'stores'

    # Define columns for the model
    id = db.Column(db.Integer, primary_key=True) # Primary Key for the store
    name = db.Column(db.String(100), nullable=False) # Name of the store
    type = db.Column(db.String(50), nullable=False) # Type of store
    location = db.Column(db.String(200), nullable=False) # Location of the store

    # Define relationship with other models
    purchase = db.relationship('Purchase', backref='stores', lazy=True) # Relationship with the Purchase model, linking stores to their purchases

    # Method to serialize Store object
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'location': self.location
        }

# Schema for serialization/deserialization of Store objects
class StoreSchema(Schema):
    id = fields.Int(dump_only=True) # ID field is read only
    name = fields.Str(required=True) # Name is required
    type = fields.Str(required=True) # Type is required
    location = fields.Str(required=True) # Location is required

# Schema for serialization/deserialization of Store objects
store_schema = StoreSchema()