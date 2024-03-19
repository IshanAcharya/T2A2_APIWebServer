from src.models import db

class User(db.Model):
    # Define table name for the model
    __tablename__ = 'users'

    # Define columns for the model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=True, nullable=False)


# Define relationships with other models
    purchase = db.relationship('Purchase', backref='user', lazy=True)
    alert = db.relationship('Alert', backref='user', lazy=True)