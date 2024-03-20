from flask import Blueprint, jsonify, request
from src.models import db
from src.models.user import User
from bcrypt import hashpw, gensalt, checkpw
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError

# Create blueprint for auth controller
auth_bp = Blueprint('auth', __name__, url_prefix="/auth")

# Function to register a new user
@auth_bp.route('/register', methods=['POST'])
def register_user():
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
    
    # Hash password using bcrypt
    hashed_password = generate_password_hash(password)
    # Create new user
    new_user = User(username=username, email=email, password=hashed_password)

    # Add new user to database 
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!'}), 201

# Function to generate password using bcrypt
def generate_password_hash(password):
    salt = gensalt()
    hashed_password = hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

# Function to log in a user
@auth_bp.route('/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Conduct check for whether email and password are provided
    if not email or not password:
        return jsonify ({'message': 'Email and password are required!'}), 400

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
@auth_bp.route('/protected', methods=['GET', 'POST'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200