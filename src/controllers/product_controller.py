from flask import Blueprint, jsonify, request
from src.models import db
from src.models.product import Product
from marshmallow import ValidationError

# Create blueprint for product controller
product_bp = Blueprint('product', __name__, url_prefix="/product")

# Function to create a new product
# http://localhost:8080/products - POST
@product_bp.route('/product', methods=['POST'])
def create_product():
    data = request.json
    name = data.get('name')
    brand = data.get('brand')
    category = data.get('category')

    try:
        # Validate input data
        if not name or not brand or not category:
            raise ValidationError('Name, brand and category are required fields!')
        
        # Check for duplicate product names
        existing_product = Product.query.filter_by(name=name).first()
        if existing_product:
            raise ValidationError('Product name already exists!')
        
        # Validate category to be alphabetical only
        if not category.isalphaa():
            raise ValidationError('Category must be alphabetical only')
        
        # Create new product object
        new_product = Product(name=name, brand=brand, category=category)

        # Add new product to database 
        db.session.add(new_product)
        db.session.commit()

        # Return success message and product ID
        return jsonify({'message': 'Product created successfully!', 'product_id': new_product.id}), 201
    except Exception as e:
        # Rollback in case of any errors
        db.session.rollback()
        return jsonify({'message': 'Failed to create product', 'error': str(e)}), 500
    
# Function to retrieve product by ID
# http://localhost:8080/products/id - GET
@product_bp.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    # Query database for product with specified ID
    product = Product.query.get(product_id)
    if product:
        # Serialise product data and return it
        return jsonify(product.serialise()), 200
    else:
        # Return error message if product not found
        return jsonify({'message': 'Product not found'}), 404
    
# Function to update product by ID
# http://localhost:8080/products/id - PUT
@product_bp.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    # Query database for product with specified ID
    product = Product.query.get(product_id)
    if product:
        try:
            # Update product attributes with new data
            for key, value in data.items():
                setattr(product, key, value)
            # Commit session
            db.session.commit()
            return jsonify({'message': 'Product updated successfully!'}), 200
        except Exception as e:
            # Rollback session if error present
            db.session.rollback()
            return jsonify({'message': 'Failed to update product', 'error': str(e)}), 500

# Function to delete product by ID
# http://localhost:8080/products/id - DELETE
@product_bp.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    # Query database for product with specified ID
    product = Product.query.get(product_id)
    if product:
        try:
            # Delete product from database
            db.session.delete(product)
            db.session.commit()
            return jsonify({'message': 'Product deleted successfully!'}), 200
        except Exception as e:
            # Rollback if error present
            db.session.rollback()
            return jsonify({'message': 'Failed to delete product', 'error': str(e)}), 500
    else: 
        # Return error message if product not found
        return jsonify({'message': 'Product not found'}), 404