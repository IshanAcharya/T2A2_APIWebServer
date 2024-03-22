from flask import Blueprint, jsonify, request
from src import db
from src.models.promotion import Promotion, PromotionSchema
from marshmallow import ValidationError

# Create blueprint for promotion controller
promotion_bp = Blueprint('promotion', __name__, url_prefix="/promotion")

# Load schema for request validation and response serialization
promotion_schema = PromotionSchema()

# Function to create a promotion
# http://localhost:8080/promotions - POST
@promotion_bp.route('/promotion', methods=['POST'])
def create_promotion():
    try:
        # Validate incoming data
        data = promotion_schema.load(request.json)
    except ValidationError as ve:
        return jsonify({'message': 'Validation error', 'error': ve.messages}), 400

    try: 
        # Check for duplicate promotions
        existing_promotion = Promotion.query.filter_by(product_id=data['product_id'], promotion_type=data['promotion_id']).first()
        if existing_promotion:
            return jsonify({'message': 'Duplicate promotion entry'}), 400
        
        # Create new promotion object
        new_promotion = Promotion(product_id=data['product_id'], promotion_type=data['promotion_type'], promotion_discount=data['promotion_discount'])

        # Add new promotion to database
        db.session.add(new_promotion)
        db.session.commit()

        # Return success message and ID of new promotion
        return jsonify({'message': 'Promotion created successfully', 'promotion_id': new_promotion.id}), 201
    except Exception as e:
        # Rollback and return if error present
        db.session.rollback()
        return jsonify({'message': 'Failed to create a promotion', 'error': str(e)}), 500

# Function to retrieve a promotion by ID
# http://localhost:8080/promotions/id - GET
@promotion_bp.route('/promotion/<int:promotion_id>', methods=['GET'])
def get_promotion(promotion_id):
    # Query database for promotion with the specified ID
    promotion = Promotion.query.get(promotion_id)
    if promotion:
        # If promotion found, serialize data
        return promotion_schema.jsonify(promotion), 200
    else:
        # Return error messsage if promotion not found
        return jsonify({'message': 'Promotion not found'}), 404

# Function to update a promotion by ID
# http://localhost:8080/promotions/id - PUT
@promotion_bp.route('/promotion/<int:promotion_id>', methods=['PUT'])
def update_promotion(promotion_id):
    # Query database for promotion with the specified ID
    promotion = Promotion.query.get(promotion_id)
    if promotion:
        try:
            # Validate incoming data
            data = promotion_schema.load(request.json, partial=True)

            # Update promotion attributes with new data 
            promotion.product_id = data.get('product_id', promotion.product_id)
            promotion.promotion_type = data.get('promotion_type', promotion.promotion_type)
            promotion.promotion_discount = data.get('promotion_discount', promotion.promotion_discount)

            # Commit changes
            db.session.commit()
            # Return success message
            return jsonify({'message': 'Promotion updated successfully'}), 200
        except ValidationError as ve:
            return jsonify({'message': 'Validation error', 'error': ve.messages}), 400
        except Exception as e:
            # Rollback and return error message if error present
            db.session.rollback()
            return jsonify({'message': 'Failed to update promotion', 'error': str(e)}), 500
    else: 
        # Return error message if promotion not found
        return jsonify({'message': 'Promotion not found'}), 404

# Function to delete promotion by ID
# http://localhost:8080/promotions/id - DELETE
@promotion_bp.route('/promotion/<int:promotion_id>', methods=['DELETE'])
def delete_promotion(promotion_id):
    # Query database for promotion with the specified ID
    promotion = Promotion.query.get(promotion_id)
    if promotion:
        try:
            # Delete promotion from database and commit changes
            db.session.delete(promotion)
            db.session.commit()

            # Return success message
            return jsonify({'message': 'Promotion deleted sucessfully'}), 200 
        except Exception as e:
            # Rollback and return error message if error present
            db.session.rollback()
            return jsonify({'message': 'Failed to delete promotion', 'error': str(e)}), 500
    else:
        # Return error message if promotion not found
        return jsonify({'message': 'Promotion not found'}), 404