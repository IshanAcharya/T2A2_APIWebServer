from src.models import db

class Store(db.Model):
    # Define table name for the model
    __tablename__ = 'store'

    # Define columns for the model
    id = db.Column(db.integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200), nullable=False)

    # Define relationship with other models
    purchase = db.relationship('Purchase', backref='store', lazy=True)

    def serialise(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'location': self.location
        }