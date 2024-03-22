from flask import Blueprint, jsonify, request
from src import db
from src.models.alert import Alert, AlertSchema
from marshmallow import ValidationError

# Create blueprint for alert controller
alert_bp = Blueprint('alert', __name__, url_prefix="/alert")

# Load schema for request validation and response serialization
alert_schema = AlertSchema()

# Function to create an alert
# http://localhost:8080/alerts - POST
@alert_bp.route('/alert', methods=['POST'])
def create_alert():
    try:
        # Validate incoming data
        data = alert_schema.load(request.json)
    except ValidationError as ve:
        return jsonify({'message': 'Validation error', 'error': ve.messages}), 400

    try:
        # Create new alert object
        new_alert = Alert(user_id=data['user_id'], product_id=data['product_id'], day_of_week=data['day_of_week'])

        # Add alert to database
        db.session.add(new_alert)
        db.session.commit()

        # Return success message with ID of newly created alert
        return jsonify({'message': 'Alert created successfully', 'alert_id': new_alert.id}), 201
    except Exception as e:
        # Rollback and return mesasge if error present
        db.session.rollback()
        return jsonify({'message': 'Failed to create an alert', 'error': str(e)}), 500

# Function to get an alert by its ID
# http://localhost:8080/alerts/id - GET
@alert_bp.route('/alert/<int:alert_id>', methods=['GET'])
def get_alert(alert_id):
    # Query database for alert with specified ID
    alert = Alert.query.get(alert_id)
    if alert: 
        # Return serialized alert data if found
        return alert_schema.jsonify(alert), 200
    else:
        # Return error message if alert not found
        return jsonify({'message': 'Alert not found'}), 404

# Function to update an alert by its ID
# http://localhost:8080/alerts/id - PUT
@alert_bp.route('/alert/<int:alert_id>', methods=['PUT'])
def update_alert(alert_id):
    data = request.json
    # Query database for alert with specified ID
    alert = Alert.query.get(alert_id)
    if alert:
        try:
            # Validate incoming data
            data = alert_schema.load(request.json, partial=True)

            # Update alert attributes with new data
            alert.user_id = data.get('user_id', alert.user_id)
            alert.product_id = data.get('product_id', alert.product_id)
            alert.day_of_week = data.get('day_of_week', alert.day_of_week)

            # Commit changes 
            db.session.commit()
            # Return success message
            return jsonify({'message': 'Alert updated successfully'}), 200
        except ValidationError as ve:
            return jsonify({'message': 'Validation error', 'error': ve.messages}), 400
        except Exception as e:
            # Rollback and return error message if error present
            db.session.rollback()
            return jsonify({'message': 'Failed to update alert', 'error': str(e)}), 500
    else:
        # Return message if alert not found
        return jsonify({'message': 'Alert not found'}), 404

# Function to delete an alert by its ID
# http://localhost:8080/alerts/id - DELETE
@alert_bp.route('/alert/<int:alert_id>', methods=['DELETE'])
def delete_alert(alert_id):
    # Query database for alert with specified ID
    alert = Alert.query.get(alert_id)
    if alert:
        try:
            # Delete alert from database
            db.session.delete(alert)
            db.session.commit()
            # Return success message
            return jsonify({'message': 'Alert deleted successfully'}), 200
        except Exception as e:
            # Rollback and return error message if error present
            db.session.rollback()
            return jsonify({'message': 'Failed to delete alert', 'error': str(e)}), 500
    else:
        # Return message if alert not found
        return jsonify({'message': 'Alert not found'}), 404