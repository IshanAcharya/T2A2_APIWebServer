from flask import Blueprint, jsonify, request
from src import db
from src.models.product import Product, ProductSchema
from marshmallow import ValidationError

# Create blueprint for product controller
product_bp = Blueprint('product', __name__, url_prefix="/product")

# Load schema for request validation and response serialization
product_schema = ProductSchema()

# Function to create a new product
# http://localhost:8080/products - POST
@product_bp.route('/product', methods=['POST'])
def create_product():
    try: 
        # Validate incoming data
        data = product_schema.load(request.json)
    except ValidationError as ve:
        return jsonify({'message': 'Validation error', 'error': ve.messages}), 400

    try:
        # Check for duplicate product names
        existing_product = Product.query.filter_by(name=data['name']).first()
        if existing_product:
            return jsonify({'message': 'Product name already exists'}), 400
        
        # Create new product object
        new_product = Product(name=data['name'], brand=data['brand'], category=data['category'])

        # Add new product to database and commit changes
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
        # Serialize product data and return it
        return product_schema.jsonify(product), 200
    else:
        # Return error message if product not found
        return jsonify({'message': 'Product not found'}), 404
    
# Function to update product by ID
# http://localhost:8080/products/id - PUT
@product_bp.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    # Query database for product with specified ID
    product = Product.query.get(product_id)
    if product:
        try:
            # Validate incoming data
            data = product_schema.load(request.json, partial=True)

            # Update product attributes with new data
            product.name = data.get('name', product.name)
            product.brand = data.get('brand', product.brand)
            product.category = data.get('category', product.category)

            # Commit session
            db.session.commit()
            return jsonify({'message': 'Product updated successfully'}), 200
        except ValidationError as ve:
            return jsonify({'message': 'Validation error', 'error': ve.messages}), 400
        except Exception as e:
            # Rollback session if error present
            db.session.rollback()
            return jsonify({'message': 'Failed to update product', 'error': str(e)}), 500
    else:
        # Return message if product not found
        return jsonify({'message': 'Product not found'}), 404

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
            return jsonify({'message': 'Product deleted successfully'}), 200
        except Exception as e:
            # Rollback if error present
            db.session.rollback()
            return jsonify({'message': 'Failed to delete product', 'error': str(e)}), 500
    else: 
        # Return error message if product not found
        return jsonify({'message': 'Product not found'}), 404