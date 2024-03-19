from flask import jsonify
from src.models import db
from src.models.alert import Alert

# Function to create an alert
def create_alert(user_id, product_id, day_of_week):
    try:
        # Create new alert object
        new_alert = Alert(user_id=user_id, product_id=product_id, day_of_week=day_of_week)

        # Add alert to database
        db.session.add(new_alert)
        db.session.commit()

        # Return success message with ID of newly created alert
        return jsonify({'message': 'Alert created successfully!', 'alert_id': new_alert.id}), 201
    except Exception as e:
        # Rollback and return error message if error present
        db.session.rollback()
        return jsonify({'message': 'Failed to create an alert', 'error': str(e)}), 500

# Function to get an alert by its ID
def get_alert(alert_id):
    # Query database for alert with specified ID
    alert = Alert.query.get(alert_id)
    if alert: 
        # Return serialised alert data if found
        return jsonify(alert.serialise()), 200
    else:
        # Return error message if alert not found
        return jsonify({'message': 'Alert not found'}), 404

# Function to update an alert
def update_alert(alert_id, new_data):
    # Query database for alert with specified ID
    alert = Alert.query.get(alert_id)
    if alert:
        try:
            # Update alert attributes with new data
            for key, value in new_data.items():
                setattr(alert, key, value)
            db.session.commit()
            # Return success message
            return jsonify({'message': 'Alert updated successfully!'}), 200
        except Exception as e:
            # Rollback and return error message if error present
            db.session.rollback()
            return jsonify({'message': 'Failed to update alert', 'error': str(e)}), 500
    else:
        # Return message if alert not found
        return jsonify({'message': 'Alert not found'}), 404

# Function to delete an alert
def delete_alert(alert_id):
    # Query database for alert with specified ID
    alert = Alert.query.get(alert_id)
    if alert:
        try:
            # Delete alert from database
            db.session.delete(alert)
            db.session.commit()
            # Return success message
            return jsonify({'message': 'Alert deleted successfully!'}), 200
        except Exception as e:
            # Rollback and return error message if error present
            db.session.rollback()
            return jsonify({'message': 'Failed to delete alert', 'error': str(e)}), 500
    else:
        # Return message if alert not found
        return jsonify({'message': 'Alert not found'}), 404