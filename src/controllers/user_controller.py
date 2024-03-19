from flask import request, jsonify
from src.models import db
from src.models.user import User

def create_user():
    # Obtain user data
    data = request.json

    # Extract user details from user data
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

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
        # Rollback if error present
        db.session.rollback()
        return jsonify({'message': 'Failed to create user', 'error': str(e)}), 500

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

