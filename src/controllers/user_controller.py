from flask import Blueprint, request, jsonify
from src.models import db
from src.models.user import User
from marshmallow import ValidationError

# Create blueprint for user controller

user_bp = Blueprint('user', __name__, url_prefix="/user")

# Function to create a new user
# http://localhost:8080/users - POST
@user_bp.route('/user', methods=['POST'])
def create_user():
    # Obtain user data
    data = request.json

    # Extract user details from user data
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Validation for username
    if not data.get('username'):
        raise ValidationError('Username is required')
    
    # Validation for email format
    if not email or '@' not in email or '.' not in email.split('@')[1]: 
        raise ValidationError('Invalid email format')
    
    # Validation for password strength
    if not password: 
        raise ValidationError('Password is required')
    elif len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long')
    elif not any(char.isdigit() for char in password):
        raise ValidationError('Password must contain at least one digit')
    elif not any(char.isalpha() for char in password):
        raise ValidationError('Password must contain at least one letter')

    # Conduct check for whether username and email are provided or not
    if not username or not email or not password:
        return jsonify({'message': 'Username, email and password are required!'}), 400

    # Conduct check for whether user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'User already exists!'}), 400
    
    try:
        # Create new user 
        new_user = User(username=username, email=email, password=password)

        # Add new user to database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully!'}), 201
    except Exception as e:
        # Rollback and return error message if error present
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
    
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email
    }

    return jsonify(user_data), 200

# Function to update a user by ID
# http://localhost:8080/users/id - PUT
@user_bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # Obtain user data from requeust
    data = request.json

    # Retrieve user to update
    user = User.query.get(user_id)

    # Conduct check to see if user already exists
    if not user: 
        return jsonify({'message': 'User not found'}), 404
    
    # Update user details
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        email = data['email']
        if not email or '@' not in email or '.' not in email.split('@')[1]: 
            raise ValidationError('Invalid email format')
        user.email = data['email']
    if 'password' in data:
        password = data['password']
        if not password:
            return jsonify({'message': 'Password is required'}), 400
        elif len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long')
        elif not any(char.isdigit() for char in password):
            raise ValidationError('Password must contain at least one digit')
        elif not any(char.isalpha() for char in password):
            raise ValidationError('Password must contain at least one letter')
        user.password = data['password']
    
    try: 
        db.session.commit()
        # Return message if user updated
        return jsonify({'message': 'User updated successfully!'}), 200
    except Exception as e:
        # Rollback and return error message if error present
        db.session.rollback()
        return jsonify ({'message': 'Failed to update user', 'error': str(e)}), 500

# Function to delete a user by ID
# http://localhost:8080/users/id - DELETE
@user_bp.route('/user/<int:user_id>', methods=['DELETE'])        
def delete_user(user_id):
    # Retrieve user to delete
    user = User.query.get(user_id)

    # Conduct check to see if user already exists
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    try: 
        # Delete user from database
        db.session.delete(user)
        db.session.commit()
        # Return message if user deleted
        return jsonify({'message': 'User deleted successfully!'}), 200
    except Exception as e:
        # Rollback and return error message if error present 
        db.session.rollback()
        return jsonify({'message': 'Failed to delete user', 'error': str (e)}), 500