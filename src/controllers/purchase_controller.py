from flask import Blueprint, jsonify, request
from src import db
from src.models.purchase import Purchase, PurchaseSchema
from marshmallow import ValidationError

# Create blueprint for purchase controller
purchase_bp = Blueprint('purchase', __name__, url_prefix="/purchase")

# Load schema for request validation and response serialization
purchase_schema = PurchaseSchema()

# Function to create a purchase
# http://localhost:8080/purchases - POST
@purchase_bp.route('/purchase', methods=['POST'])
def create_purchase():
    try:
        # Validate incoming data
        data = purchase_schema.load(request.json)
    except ValidationError as ve:
        return jsonify({'message': 'Validation error', 'error': ve.messages}), 400
    
    # Check for duplicate product entries
    existing_purchase = Purchase.query.filter_by(user_id=data['user_id'], product_id=data['product_id'], store_id=data['store_id']).first()
    if existing_purchase: 
        return jsonify({'message': 'Duplicate purchase entry'}), 400
                                                 
    try: 
        # Create new purchase object
        new_purchase = Purchase(
            user_id=data['user_id'],
            product_id=data['product_id'],
            store_id=data['store_id'],
            price=data['price'],
            purchase_date=data['purchase_date'],
            promotion_id=data.get('promotion_id')
        )
    
        # Conduct check to ensure that the price is a positive value 
        if new_purchase.price <= 0:
            raise ValidationError('Price must be a positive value')

        # Add new purchase to database
        db.session.add(new_purchase)
        db.session.commit()

        # Return success message with ID of new created purchase
        return jsonify({'message': 'Purchase created successfully!', 'purchase_id': new_purchase.id}), 201
    except Exception as e:
        # Rollback transaction if error present
        db.session.rollback()
        return jsonify({'message': 'Failed to created a purchase', 'error': str(e)}), 500

# Function to retrieve a purchase by ID
# http://localhost:8080/purchases/id - GET
@purchase_bp.route('/purchase/<int:purchase_id>', methods=['GET'])    
def get_purchase(purchase_id):
    # Query database for purchase with specified ID
    purchase = Purchase.query.get(purchase_id)
    if purchase:
        # Serialize purchase data and return it
        return purchase_schema.jsonify(purchase), 200
    else:
        return jsonify({'message': 'Purchase not found'}), 404

# Function to update a purchase by ID
# http://localhost:8080/purchases/id - PUT
@purchase_bp.route('/purchase/<int:purchase_id>', methods=['PUT'])     
def update_purchase(purchase_id):
    # Query database for the purchase with the specified ID
    purchase = Purchase.query.get(purchase_id)
    if purchase:
        try:
            # Validate incoming data
            data = purchase_schema.load(request.json, partial=True)

            # Update purchase attributes based on new data
            purchase.user_id = data.get('user_id', purchase.user_id)
            purchase.product_id = data.get('product_id', purchase.product_id)
            purchase.store_id = data.get('store_id', purchase.store_id)
            purchase.price = data.get('price', purchase.price)
            purchase.purchase_date = data.get('purchase_date', purchase.purchase_date)
            purchase.promotion_id = data.get('promotion_id', purchase.promotion_id)
            
            # Commit changes
            db.session.commit()
            # Return message
            return jsonify({'message': 'Purchase updated successfully'}), 200
        except ValidationError as ve:
            return jsonify({'message': 'Validation Error', 'error': str(ve)}), 400
        except Exception as e:
            # Rollback transaction if error present
            db.session.rollback()
            return jsonify({'message': 'Failed to update purchase', 'error': str(e)}), 500
    else: 
        return jsonify({'message': 'Purchase not found'}), 404

# Function to delete a purchase by ID
# http://localhost:8080/purchases/id - DELETE
@purchase_bp.route('/purchase/<int:purchase_id>', methods=['DELETE']) 
def delete_purchase(purchase_id):
    # Query database for the purchase with the specified ID
    purchase = Purchase.query.get(purchase_id)
    if purchase:
        try:
            # Delete purchase from the database and commit changes
            db.session.delete(purchase)
            db.session.commit()
            return jsonify({'message': 'Purchase deleted successfully'}), 200
        except Exception as e:
            # Rollback transaction if error present
            db.session.rollback()
            return jsonify({'message': 'Failed to delete purchase', 'error': str(e)}), 500
    else:
        return jsonify({'message': 'Purchase not found'}), 404