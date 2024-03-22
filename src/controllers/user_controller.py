from flask import Blueprint, request, jsonify
from src import db
from src.models.user import User, UserSchema
from marshmallow import ValidationError

# Create blueprint for user controller

user_bp = Blueprint('user', __name__, url_prefix="/user")

# Load schema for request validation
user_schema = UserSchema()

# Function to create a new user
# http://localhost:8080/users - POST
@user_bp.route('/user', methods=['POST'])
def create_user():
    try: 
        # Deserialize data using schema
        user_data = user_schema.load(request.json)

        # Conduct check for whether user already exists
        existing_user = User.query.filter_by(email=user_data['email']).first()
        if existing_user:
            return jsonify({'message': 'User already exists!'}), 400
    
        # Create new user object with deserialised data
        new_user = User(**user_data)

        # Add and commit new user to database
        db.session.add(new_user)
        db.session.commit()

        # Serialize created user object
        serialized_user = user_schema.dump(new_user)
        return jsonify({'message': 'User created successfully!'}), 201
    
    except ValidationError as e:
        # Handle validation errors
        return jsonify({'error': e.messages}), 400

    except Exception as e:
        # Handle other exceptions
        db.session.rollback()
        return jsonify({'message': 'Failed to create user', 'error': str(e)}), 500

# Function to retrieve a user by ID
# http://localhost:8080/users/id - GET
@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Retrieve user from databased
    user = User.query.get(user_id)

    # Conduct check to see if the user exists
    if not user:
        return jsonify({'message:' 'User not found'}), 404
    
    # Serialize user object
    serialized_user = user_schema.dump(user)

    return jsonify(serialized_user), 200

# Function to update a user by ID
# http://localhost:8080/users/id - PUT
@user_bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try: 
    
        # Retrieve user to update from 
        user = User.query.get(user_id)

        # Conduct check to see if user already exists
        if not user: 
            return jsonify({'message': 'User not found'}), 404
    
        # Deserialise data using schema
        user_data = user_schema.load(request.json)

        # Update user object 
        for key, value in user_data.items():
            setattr(user, key, value)

        # Commit change to database
        db.session.commit()

        return jsonify({'message': 'User updated successfully!'}), 200

    except ValidationError as e:
        # Handle validation errors
        return jsonify({'error': e.messages}), 400
    
    except Exception as e:
        # Handle other exceptions
        db.session.rollback()
        return jsonify ({'message': 'Failed to update user', 'error': str(e)}), 500

# Function to delete a user by ID
# http://localhost:8080/users/id - DELETE
@user_bp.route('/user/<int:user_id>', methods=['DELETE'])        
def delete_user(user_id):
    # Retrieve user to delete from database
    user = User.query.get(user_id)

    # Conduct check to see if user already exists
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    try: 
        # Delete user from database and commit change
        db.session.delete(user)
        db.session.commit()
        # Return message if user deleted
        return jsonify({'message': 'User deleted successfully!'}), 200
    
    except Exception as e:
        # Handle exceptions
        db.session.rollback()
        return jsonify({'message': 'Failed to delete user', 'error': str (e)}), 500