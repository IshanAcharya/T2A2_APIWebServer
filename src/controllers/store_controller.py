from flask import Blueprint, jsonify, request
from src import db
from src.models.store import Store, StoreSchema
from marshmallow import ValidationError

# Create blueprint for store controller
store_bp = Blueprint('store', __name__, url_prefix="store")

# Load schema for request validation and response serialization
store_schema = StoreSchema()

# Function to create a new store
# http://localhost:8080/stores - POST
@store_bp.route('/store', methods=['POST'])
def create_store():
    try:
        # Validate incoming data
        data = store_schema.load(request.json)
    except ValidationError as e:
        return jsonify({'message': 'Validation Error', 'error': str(e)}), 400
    
    # Check if store with same name already exists
    existing_store = Store.query.filter_by(name=data['name']).first()
    if existing_store: 
        return jsonify({'message': 'Store with the same name already exists'}), 400
    
    try: 
        # Create new store object
        new_store = Store(name=data['name'], type=data['type'], location=data['location'])
    
        # Add new store to database and commit changes
        db.session.add(new_store)
        db.session.commit()

        # Return success message with ID of newly created store
        return jsonify({'message': 'Store created successfully', 'store_id': new_store.id}), 201
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
        return store_schema.jsonify(store), 200
    else:
        # Return error message if store not found
        return jsonify({'message': 'Store not found'}), 404

# Function to update a store
# http://localhost:8080/stores/id - PUT
@store_bp.route('/store/<int:store_id>', methods=['PUT'])
def update_store(store_id, new_data):
    # Query database for store with specified ID
    store = Store.query.get(store_id)
    if store:
        try:
            # Validate incoming data
            data = store_schema.load(request.json, partial=True)

            # Update store attributes with new data
            store.name = data.get('name', store.name)
            store.type = data.get('type', store.type)
            store.location = data.get('location', store.location)

            # Commit changes 
            db.session.commit()

            # Return success message
            return jsonify({'message': 'Store updated successfully!'}), 200
        except ValidationError as e: 
            return jsonify({'message': 'Validation Error', 'error': str(e)}), 400
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