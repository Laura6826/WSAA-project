from flask import Flask, request, jsonify, render_template
import requests
import logging
from dao.car_parks_dao import CarParksDAO
from dao.opening_hours_dao import OpeningHoursDAO
from schemas import CarParkSchema
from marshmallow import ValidationError

app = Flask(__name__, static_folder='static')

# DAO instances
car_parks_dao = CarParksDAO()
opening_hours_dao = OpeningHoursDAO()

# External API details
API_URL = "https://data.corkcity.ie/en_GB/api/3/action/datastore_search_sql"
RESOURCE_ID = "f4677dac-bb30-412e-95a8-d3c22134e3c0"

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Root endpoint
# Check if the API is reachable; http://127.0.0.1:5000/
@app.route('/')
def index():
    logging.debug("Serving the Parking Checker HTML file.")
    return render_template('parking_checker.html')

# Existing API: Fetch live parking data
# curl -X GET http://127.0.0.1:5000/api/fetch
@app.route('/api/fetch', methods=['GET'])
def fetch_parking_data():
    sql_query = f"""SELECT * FROM "{RESOURCE_ID}" """
    try:
        params = {"sql": sql_query}
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        records = data.get("result", {}).get("records", [])
        return jsonify(records), 200
    except Exception as e:
        logging.error(f"Error fetching parking data: {e}")
        return jsonify({"error": str(e)}), 500

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
# curl -X POST -H "Content-Type: application/json" -d '{"name": "Test Car Park", "height": 2.5}' http://127.0.0.1:5000/api/car-parks
@app.route('/api/car-parks', methods=['POST'])
def create_car_park():
    try:
        # Load and validate incoming data
        data = request.json
        name = data.get("name")
        height = data.get("height")

        # Validate input
        if not name or not height:
            return jsonify({"error": "Name and height are required"}), 400

        result = car_parks_dao.create_car_park(name, height)
        if result:
            return jsonify({"message": "Car park created successfully"}), 201
        else:
            return jsonify({"error": "Failed to create car park"}), 500
    except Exception as e:
        logging.error(f"Error creating car park: {e}")
        return jsonify({"error": str(e)}), 500

# Update a car park
# curl -X PUT -H "Content-Type: application/json" -d '{"name": "Updated Car Park", "height": 3.0}' http://127.0.0.1:5000/api/car-parks/1
@app.route('/api/car-parks', methods=['POST'])
def create_car_park():
    try:
        # Load and validate incoming data
        data = request.json
        schema = CarParkSchema()
        validated_data = schema.load(data)  # Validates and deserializes the input
        
        # Extract data
        name = validated_data.get("name")
        height = validated_data.get("height")
        opening_hours = validated_data.get("opening_hours")
        
        # Save car park to database
        car_park_id = car_parks_dao.create_car_park(name, height)
        
        # Save opening hours to database
        for hours in opening_hours:
            opening_hours_dao.add_opening_hours(
                car_park_id, hours["day"], hours["opening_time"], hours["closing_time"], hours.get("status")
            )
        
        return jsonify({"message": "Car park created successfully"}), 201

    except ValidationError as err:
        # Return validation errors
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        # Handle other exceptions
        logging.error(f"Error creating car park: {e}")
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
        opening_hours = opening_hours_dao.get_opening_hours_for_car_park(car_park_id)
        return jsonify(opening_hours), 200
    except Exception as e:
        logging.error(f"Error fetching opening hours: {e}")
        return jsonify({"error": str(e)}), 500

# Add opening hours for a car park
# curl -X POST -H "Content-Type: application/json" -d '{"car_park_id": 1, "day": "Monday", "opening_time": "06:00", "closing_time": "20:00", "status": ""}' http://127.0.0.1:5000/api/opening-hours
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
        if not car_park_id or not day or not (opening_time or closing_time or status):
            return jsonify({"error": "All fields are required"}), 400

        result = opening_hours_dao.add_opening_hours(car_park_id, day, opening_time, closing_time, status)
        if result:
            return jsonify({"message": "Opening hours added successfully"}), 201
        else:
            return jsonify({"error": "Failed to add opening hours"}), 500
    except Exception as e:
        logging.error(f"Error adding opening hours: {e}")
        return jsonify({"error": str(e)}), 500

# Update opening hours for a car park
# curl -X PUT -H "Content-Type: application/json" -d '{"day": "Monday", "opening_time": "07:00", "closing_time": "21:00", "status": ""}' http://127.0.0.1:5000/api/opening-hours/1
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
            return jsonify({"message": "Opening hours updated successfully"}), 200
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
            return jsonify({"message": "Opening hours deleted successfully"}), 200
        else:
            return jsonify({"error": "Opening hours not found"}), 404
    except Exception as e:
        logging.error(f"Error deleting opening hours: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    logging.debug("Starting the Flask server...")
    app.run(debug=True)