from flask import Blueprint, jsonify, request
from src import db
from src.models.user import User
from bcrypt import hashpw, gensalt, checkpw
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError

# Create blueprint for auth controller
auth_bp = Blueprint('auth', __name__, url_prefix="/auth")

# Function to register a new user
# http://localhost:8080/auth/register - POST
@auth_bp.route('/register', methods=['POST'])
def register_user():
    # Obtain user data
    data = request.json

    # Extract user details from user data
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    try:
        # Validate input data
        if not username:
            raise ValidationError('Username is required')
        if not email:
            raise ValidationError('Email is required')
        if not password:
            raise ValidationError('Password is required')

        # Conduct check for whether user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'message': 'User already exists!'}), 400
    
        # Hash password using bcrypt
        hashed_password = generate_password_hash(password)
        # Create new user
        new_user = User(username=username, email=email, password=hashed_password)

        # Add new user to database 
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully!'}), 201
    except ValidationError as e:
        return jsonify({'message': 'Validation Error', 'error': str(e)}), 400
    except Exception as e:
        # Rollback and return error message if error present
        db.session.rollback()
        return jsonify({'message': 'Failed to register user', 'error': str(e)}), 500

# Function to generate password using bcrypt
def generate_password_hash(password):
    salt = gensalt()
    hashed_password = hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

# Function to log in a user
# http://localhost:8080/auth/login - POST
@auth_bp.route('/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Validate input data
    if not email:
        raise ValidationError('Email is required')
    if not password: 
        raise ValidationError('Password is required')

    # Query database for user 
    user = User.query.filter_by(email=email).first()

    # Conduct check for whether the user already exists and if the password is correct
    if not user or not checkpw(password.encode('utf-8'), (user.password, password)):
        return jsonify({'message': 'Invalid email or password!'}), 401

    # Generate access token using Flask JWT Extended
    access_token = create_access_token(identity=user.id)
    # Return access token
    return jsonify({'access_token': access_token}), 200

# Function to authenticate a user
# http://localhost:8080/auth/protected - GET/POST
@auth_bp.route('/protected', methods=['GET', 'POST'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200