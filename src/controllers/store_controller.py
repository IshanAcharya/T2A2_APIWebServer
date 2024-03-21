from flask import Blueprint, jsonify, request
from src.models import db
from src.models.store import Store
from marshmallow import ValidationError

# Create blueprint for store controller
store_bp = Blueprint('store', __name__, url_prefix="store")

# Function to create a new store
# http://localhost:8080/stores - POST
@store_bp.route('/store', methods=['POST'])
def create_store():
    data = request.json

    name = data.get('name')
    type = data.get('type')
    location = data.get('location')

    # Validate data

    if 'name' not in data:
        raise ValidationError('Store name is required')
    if 'type' not in data:
        raise ValidationError('Store type is required')
    if 'location' not in data:
        raise ValidationError('Store location is required')
    
    # Validate type field
    if not isinstance(type, str):
        raise ValidationError('Type must be a string')
    if any(char.isdigit() for char in type):
        raise ValidationError('Type cannot contain numbers')
    
    # Check if store with same name already exists
    existing_store = Store.query.filter_by(name=name).first()
    if existing_store: 
        return jsonify({'message': 'Store with the same name already exists!'}), 400

    try:
        # Create new store object
        new_store = Store(name=name, type=type, location=location)

        # Add new store to database
        db.sesion.add(new_store)
        db.session.commit()

        # Return success message with ID of newly created store
        return jsonify({'message': 'Store created successfully!', 'store_id': new_store.id}), 201
    except Exception as e:
        # Rollback and error message in case of error present
        db.session.rollback()
        return jsonify({'message': 'Failed to create a store', 'error': str(e)}), 500
    
# Function to get a store by its ID
# http://localhost:8080/stores/id - GET
@store_bp.route('/store/<int:store_id>', methods=['GET'])
def get_store(store_id):
    # Query database for store with specified ID
    store = Store.query.get(store_id)
    if store:
        # Serialise data if store is found and return it
        return jsonify(store.serialise()), 200
    else:
        # Return error message if store not found
        return jsonify({'message': 'Store not found'}), 404

# Function to update a store
# http://localhost:8080/stores/id - PUT
@store_bp.route('/store/<int:store_id>', methods=['PUT'])
def update_store(store_id, new_data):
    # Query database for store with specified ID
    data = request.json
    store = Store.query.get(store_id)
    if store:
        try:
            # Update store attributes with new data
            for key, value in new_data.items():
                setattr(store, key, value)
            db.session.commit()

            # Return success message
            return jsonify({'message': 'Store updated successfully!'}), 200
        except Exception as e:
            # Rollback and return message if error present
            db.session.rollback()
            return jsonify({'message': 'Failed to update store', 'error': str(e)}), 500
    else:
        # Return error message if store not found
        return jsonify({'message': 'Store not found'}), 404

# Function to delete a store
# http://localhost:8080/stores/id - DELETE    
@store_bp.route('/store/<int:store_id>', methods=['DELETE'])
def delete_store(store_id):
    # Query database for store with specified ID
    store = Store.query.get(store_id)
    if store:
        try:
            # Delete store from database
            db.session.delete(store)
            db.session.commit()
            # Return success message
            return jsonify({'message': 'Store deleted successfully!'}), 200
        except Exception as e:
            # Rollback and return message if error present
            db.session.rollback()
            return jsonify({'message': 'Failed to delete store', 'error': str(e)}), 500
    else:
        # Return error message if store not found
        return jsonify({'message': 'Store not found'}), 404