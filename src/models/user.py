from src.models import db

class User(db.Model):
    __tablename__ = 'users'


    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=True, nullable=False)


# Define relationships with other models
    purchases = db.relationship('Purchase', backref='user', lazy=True)
    alerts = db.relationship('Alert', backref='user', lazy=True)