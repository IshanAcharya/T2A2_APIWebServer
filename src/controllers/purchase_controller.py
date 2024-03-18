from flask import jsonify
from src.models import db
from src.models.purchase import Purchase

# Function to create a purchase
def create_purchase(user_id, product_id, store_id, price, purchase_date, promotion_id=None):
    try:
        # Conduct check to ensure that the price is positive
        if price <= 0:
            return jsonify({'message': 'Price must be a positive value'}), 400
        
        # Create new purchase object
        new_purchase = Purchase(user_id=user_id, product_id=product_id, store_id=store_id, price=price, purchase_date=purchase_date, promotion_id=promotion_id)
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
def get_purchase(purchase_id):
    # Query database for purchase with specified ID
    purchase = Purchase.query.get(purchase_id)
    if purchase:
        # Serialise purchase data and return it
        return jsonify(purchase.serialise()), 200
    else:
        return jsonify({'message': 'Purchase not found'}), 404

# Function to update a purchase
def update_purchase(purchase_id, new_data):
    # Query database for the purchase with the specified ID
    purchase = Purchase.query.get(purchase_id)
    if purchase:
        try:
            # Update purchase attributes based on new data
            for key, value in new_data.items():
                setattr(purchase, key, value)
            db.session.commit()
            return jsonify({'message': 'Purchase updated successfully!'}), 200
        except Exception as e:
            # Rollback transaction if error present
            db.session.rollback()
            return jsonify({'message': 'Failed to update purchase', 'error': str(e)}), 500
    else: 
        return jsonify({'message': 'Purchase not found'}), 404

# Function to delete a purchase    
def delete_purchase(purchase_id):
    # Query database for the purchase with the specified ID
    purchase = Purchase.query.get(purchase_id)
    if purchase:
        try:
            # Delete purchase from the database
            db.session.delete(purchase)
            db.session.commit()
            return jsonify({'message': 'Purchase deleted successfully!'}), 200
        except Exception as e:
            # Rollback transaction if error present
            db.session.rollback()
            return jsonify({'message': 'Failed to delete purchase', 'error': str(e)}), 500
    else:
        return jsonify({'message': 'Purchase not found'}), 404
