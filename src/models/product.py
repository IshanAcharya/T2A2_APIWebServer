from src.models import db

class Product(db.Model):
    # Define table name for the model
    __tablename__ = 'product'

    # Define columns for the model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100))
    category = db.Column(db.String(100))

    # Define relationships with other models
    purchase = db.relationship('Purchase', backref='product', lazy=True)
    alert = db.relationship('Alert', backref='product', lazy=True)
    promotion = db.relationship('Promotion', backref='product', lazy=True)

    def serialise(self):
        return{
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'category': self.category
        }
    
    # Ensure product names are unique
    __table_args__ = (db.UniqueConstraint('name', 'brand', 'category', name='unique_product'),)

    @classmethod
    def create(cls, name, brand, category):
        # Conduct check if product with the same name, brand and category already exists in database
        existing_product = cls.query.filter(func.lower(cls.name) == func.lower(name),
                                            func.lower(cls.brand) == func.lower(brand),
                                            func.lower(cls.category) == func.lower(category)).first()
        if existing_product:
            raise ValueError("Product with the same name, brand and category already exists!")
        
        # Create and add new product to database
        new_product = cls(name=name, brand=brand, category=category)
        db.session.add(new_product)
        db.session.commit()
        return new_product
    