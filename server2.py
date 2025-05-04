import logging
import requests
import json 
from flask import Flask, request, jsonify, render_template
from schema.schema import CarParkSchema, OpeningHoursSchema
from marshmallow import ValidationError

app = Flask(__name__, static_folder='static')

from dao.car_parks_dao import CarParksDAO
from dao.opening_hours_dao import OpeningHoursDAO
from dao.live_spaces_dao import LiveSpacesDAO

# DAO instances
car_parks_dao = CarParksDAO()
opening_hours_dao = OpeningHoursDAO()
live_spaces_dao = LiveSpacesDAO()

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Root endpoint
# Check if the API is reachable; http://127.0.0.1:5000/

@app.route('/')
def index():
    logging.debug("Serving the Parking Checker HTML file.")
    return render_template('parking_checker2.html')

# Existing API: Fetch live parking data
# curl -X GET http://127.0.0.1:5000/api/fetch

@app.route('/api/car-parks', methods=['GET'])
def get_car_parks():
    car_parks = car_parks_dao.get_all_car_parks()  # ✅ Ensure car_parks is correctly retrieved
    live_data = live_spaces_dao.fetch_live_spaces()

    logging.debug("🔍 Full Live API Response: %s", json.dumps(live_data, indent=2))  

    for park in car_parks:
        park_id = str(park["id"])  # Convert database ID to string

        # ✅ Debugging: Print each car park ID before merging
        logging.debug("🔍 Checking park ID: %s", park_id)

        # ✅ Debug live API entry format before merging
        for item in live_data:
            logging.debug("🔍 Live API item structure: %s", item)

        # ✅ Update key name to match live API structure
        park["free_spaces"] = next(
            (item.get("free_spaces", "Unavailable") for item in live_data if str(item.get("car_park_id")) == park_id),
            "Unavailable"
        )

    return jsonify(car_parks)

# Fetch live parking data for a specific car park
# curl -X GET http://
@app.route('/api/car-parks/<int:car_park_id>', methods=['GET'])
def get_car_park_availability(car_park_id):
    # Fetch static car park details
    car_park = next((park for park in car_parks_dao.get_all_car_parks() if park["id"] == car_park_id), None)
    if not car_park:
        return jsonify({"error": "Car park not found"}), 404

    # Fetch live availability data
    live_data = live_spaces_dao.fetch_live_spaces()
    car_park["free_spaces"] = next((item.get("free_spaces", "Unavailable") for item in live_data if item.get("id") == str(car_park_id)), "Unavailable")

    return jsonify(car_park)

# CRUD operations for Car Parks
# Fetch all car parks

@app.route('/api/car-parks', methods=['GET'])
def fetch_all_car_parks():
    try:
        car_parks = car_parks_dao.get_all_car_parks()
        return jsonify(car_parks), 200
    except Exception as e:
        logging.error(f"Error fetching car parks: {e}")
        return jsonify({"error": str(e)}), 500

# Create a new car park
# curl -X POST -H "Content-Type: application/json" -d '{"name": "Test Car
# Park", "height": 2.5}' http://127.0.0.1:5000/api/car-parks

@app.route('/api/car-parks', methods=['POST'])
def create_car_park():
    try:
        data = request.json
        schema = CarParkSchema()
        validated_data = schema.load(data)

        name = validated_data.get("name")
        height = validated_data.get("height")
        opening_hours = validated_data.get("opening_hours")

        car_park_id = car_parks_dao.create_car_park(name, height)
        for hours in opening_hours:
            opening_hours_dao.add_opening_hours(
                car_park_id, hours["day"], hours["opening_time"], hours["closing_time"], hours.get(
                    "status")
            )
        return jsonify({"message": "Car park created successfully"}), 201

    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        logging.error(f"Error creating car park: {e}")
        return jsonify({"error": str(e)}), 500

# Update a car park
# curl -X PUT -H "Content-Type: application/json" -d '{"name": "Updated
# Car Park", "height": 3.0}' http://127.0.0.1:5000/api/car-parks/1

@app.route('/api/car-parks/<int:car_park_id>', methods=['PUT'])
def update_car_park(car_park_id):
    """
    Updates an existing car park with new details.

    Args:
        car_park_id (int): The ID of the car park to update.

    Returns:
        JSON response: Success or failure message.
    """
    try:
        data = request.json
        schema = CarParkSchema()
        validated_data = schema.load(data)

        # Extract data
        name = validated_data.get("name")
        height = validated_data.get("height")
        opening_hours = validated_data.get("opening_hours")

        # Check if car park exists before updating
        existing_car_park = car_parks_dao.get_car_park_by_id(car_park_id)
        if not existing_car_park:
            return jsonify({"error": "Car park not found"}), 404

        # Update car park details
        result = car_parks_dao.update_car_park(car_park_id, name, height)

        # Update opening hours
        for hours in opening_hours:
            opening_hours_dao.update_opening_hours(
                car_park_id, hours["day"], hours["opening_time"], hours["closing_time"], hours.get("status")
            )

        if result:
            return jsonify({"message": "Car park updated successfully"}), 200
        else:
            return jsonify({"error": "Failed to update car park"}), 500

    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        logging.error("Error updating car park: %s", e)
        return jsonify({"error": str(e)}), 500

# Delete a car park
# curl -X DELETE http://127.0.0.1:5000/api/car-parks/1

@app.route('/api/car-parks/<int:car_park_id>', methods=['DELETE'])
def delete_car_park(car_park_id):
    try:
        result = car_parks_dao.delete_car_park(car_park_id)
        if result:
            return jsonify({"message": "Car park deleted successfully"}), 200
        else:
            return jsonify({"error": "Car park not found"}), 404
    except Exception as e:
        logging.error(f"Error deleting car park: {e}")
        return jsonify({"error": str(e)}), 500

# CRUD operations for Opening Hours
# Fetch opening hours for a specific car park

@app.route('/api/opening-hours/<int:car_park_id>', methods=['GET'])
def fetch_opening_hours(car_park_id):
    try:
        opening_hours = opening_hours_dao.get_opening_hours_for_car_park(
            car_park_id)
        return jsonify(opening_hours), 200
    except Exception as e:
        logging.error(f"Error fetching opening hours: {e}")
        return jsonify({"error": str(e)}), 500

# Add opening hours for a car park
# curl -X POST -H "Content-Type: application/json" -d '{"car_park_id": 1,
# "day": "Monday", "opening_time": "06:00", "closing_time": "20:00",
# "status": ""}' http://127.0.0.1:5000/api/opening-hours

@app.route('/api/opening-hours', methods=['POST'])
def add_opening_hours():
    try:
        data = request.json
        car_park_id = data.get("car_park_id")
        day = data.get("day")
        opening_time = data.get("opening_time")
        closing_time = data.get("closing_time")
        status = data.get("status")

        # Validate input
        if not car_park_id or not day or not (
                opening_time or closing_time or status):
            return jsonify({"error": "All fields are required"}), 400

        result = opening_hours_dao.add_opening_hours(
            car_park_id, day, opening_time, closing_time, status)
        if result:
            return jsonify(
                {"message": "Opening hours added successfully"}), 201
        else:
            return jsonify({"error": "Failed to add opening hours"}), 500
    except Exception as e:
        logging.error(f"Error adding opening hours: {e}")
        return jsonify({"error": str(e)}), 500

# Update opening hours for a car park
# curl -X PUT -H "Content-Type: application/json" -d '{"day": "Monday",
# "opening_time": "07:00", "closing_time": "21:00", "status": ""}'
# http://127.0.0.1:5000/api/opening-hours/1

@app.route('/api/opening-hours/<int:opening_hours_id>', methods=['PUT'])
def update_opening_hours(opening_hours_id):
    try:
        # Load and validate incoming data
        data = request.json
        schema = OpeningHoursSchema()
        validated_data = schema.load(data)

        # Extract data
        day = validated_data["day"]
        opening_time = validated_data["opening_time"]
        closing_time = validated_data["closing_time"]
        status = validated_data.get("status")

        # Update in database
        result = opening_hours_dao.update_opening_hours(
            opening_hours_id, day, opening_time, closing_time, status
        )
        if result:
            return jsonify(
                {"message": "Opening hours updated successfully"}), 200
        else:
            return jsonify({"error": "Opening hours not found"}), 404

    except ValidationError as err:
        # Return validation errors
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        logging.error(f"Error updating opening hours: {e}")
        return jsonify({"error": str(e)}), 500

# Delete opening hours for a car park
# curl -X DELETE http://127.0.0.1:5000/api/opening-hours/1

@app.route('/api/opening-hours/<int:opening_hours_id>', methods=['DELETE'])
def delete_opening_hours(opening_hours_id):
    try:
        result = opening_hours_dao.delete_opening_hours(opening_hours_id)
        if result:
            return jsonify(
                {"message": "Opening hours deleted successfully"}), 200
        else:
            return jsonify({"error": "Opening hours not found"}), 404
    except Exception as e:
        logging.error(f"Error deleting opening hours: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting Flask server on http://127.0.0.1:5000")
    app.run(debug=True)