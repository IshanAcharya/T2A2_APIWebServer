from flask import Flask
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# JWT Manager initilisation
jwt = JWTManager(app)

# Configure JWT secret key
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

# Configure JWT settings

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 60 * 60 * 24  # Access token expires in 1 day
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 60 * 60 * 24 * 30 # Refresh token expires in 30 days
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies'] # Identifies where JWT tokens are located

# Define route for authentication
@app.route('/protected')
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

