from flask import jsonify
from src.models import db
from src.models.product import Product

# Function to create a new product
def create_product(name, brand, category):
    try:
        # Validate input data
        if not name or not brand or not category:
            return jsonify({'message': 'Name, brand and category are required fields!'}), 400
        
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
    
# Function to retrieve product information
def get_product(product_id):
    # Query database for product with specified ID
    product = Product.query.get(product_id)
    if product:
        # Serialise product data and return it
        return jsonify(product.serialise()), 200
    else:
        # Return error message if product not found
        return jsonify({'message': 'Product not found'}), 404
    
def update_product(product_id, new_data):
    # Query database for product with specified ID
    product = Product.query.get(product_id)
    if product:
        try:
            # Update product attributes with new data
            for key, value in new_data.items():
                setattr(product, key, value)
            # Commit session
            db.session.commit()
            return jsonify({'message': 'Product updated successfully!'}), 200
        except Exception as e:
            # Rollback session if error present
            db.session.rollback()
            return jsonify({'message': 'Failed to update product', 'error': str(e)}), 500

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