from flask import jsonify
from src.models import db
from src.models.promotion import Promotion

# Function to create new promotion
def create_promotion(product_id, promotion_type, promotion_discount):
    try: 
        # Create new promotion object
        new_promotion = Promotion(product_id=product_id, promotion_type=promotion_type, promotion_discount=promotion_discount)

        # Add new promotion to database
        db.session.add(new_promotion)
        db.session.commit()

        # Return success message and ID of new promotion
        return jsonify({'message': 'Promotion created successfully!', 'promotion_id': new_promotion.id}), 200
    except Exception as e:
        # Rollback and return if error present
        db.session.rollback()
        return jsonify({'message': 'Failed to create a promotion', 'error': str(e)}), 500

def get_promotion(promotion_id):
    # Query database for promotion with the specified ID
    promotion = Promotion.query.get(promotion_id)
    if promotion:
        # If promotion found, serialise and return it along with success message
        return jsonify(promotion.serialise()), 200
    else:
        # Return error messsage if promotion not found
        return jsonify({'message': 'Promotion not found'}), 404

def update_promotion(promotion_id, new_data):
    # Query database for promotion with the specified ID
    promotion = Promotion.query.get(promotion_id)
    if promotion:
        try:
            # Update promotion object with new data
            for key, value in new_data.items():
                setattr(promotion, key, value)
            db.session.commit()

            # Return success message
            return jsonify({'message': 'Promotion updated successfully!'}), 200
        except Exception as e:
            # Rollback and return error message if error present
            db.session.rollback()
            return jsonify({'message': 'Failed to update promotion', 'error': str(e)}), 500
    else: 
        # Return error message if promotion not found
        return jsonify({'message': 'Promotion not found'}), 404


def delete_promotion(promotion_id):
    # Query database for promotion with the specified ID
    promotion = Promotion.query.get(promotion_id)
    if promotion:
        try:
            # Delete promotion from database
            db.session.delete(promotion)
            db.session.commit()

            # Return success message
            return jsonify({'message': 'Promotion deleted sucessfully!'}), 200 
        except Exception as e:
            # Rollback and return error message if error present
            db.session.rollback()
            return jsonify({'message': 'Failed to delete promotion', 'error': str(e)}), 500
    else:
        # Return error message if promotion not found
        return jsonify({'message': 'Promotion not found'}), 404