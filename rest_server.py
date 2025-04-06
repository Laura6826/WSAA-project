# WSAA-project: Web Services and Applications.
# Main Flask application
# Author: Laura Lyons

from flask import Flask, request, jsonify
from flask_caching import Cache
from db_setup import init_db, Parking
from parking_dao import ParkingDAO
import requests

# Initialize Flask app and database
app = Flask(__name__)
# Ensure database and tables are initialized
init_db()
parking_dao = ParkingDAO()

# Configure caching
app.config['CACHE_TYPE'] = 'SimpleCache'  # Use simple in-memory caching
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout in seconds (e.g., 300 seconds = 5 minutes)
cache = Cache(app)

# External API details
API_URL = "https://data.corkcity.ie/en_GB/api/3/action/datastore_search_sql"
# To test that the root is working
# curl http://127.0.0.1:5000/

@app.route('/')
def index():
    return "Welcome to the Parking Management API!"

# Fetch data from the external API with caching
# curl -X GET http://127.0.0.1:5000/api/fetch
@app.route('/api/fetch', methods=['GET'])
@cache.cached()  # Cache the response of this endpoint
def fetch_parking_data():
    query = """SELECT idd, name AS parking_name, spaces AS spaces_available, free_spaces, opening_times,
               height_restrictions AS height_restriction, price AS prices_rates, latitude, longitude 
               FROM "c609d229-f7fe-4da9-a065-1e44f65bc7dc" """
    try:
        response = requests.get(API_URL, params={"sql": query})
        if response.status_code != 200:
            return jsonify({"error": f"Failed to fetch data. HTTP Status Code: {response.status_code}"}), response.status_code
        data = response.json()
        records = data.get("result", {}).get("records", [])
        for record in records:
            parking = Parking(**record)
            parking_dao.add(parking)
        return jsonify({"message": "Data fetched and stored in the database.", "data": records}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# CRUD endpoints
# Get all parking records
# curl -X GET http://127.0.0.1:5000/api/parking
@app.route('/api/parking', methods=['GET'])
def get_all_parking():
    records = parking_dao.fetch_all()
    data = [{"idd": r.idd, "parking_name": r.parking_name, "spaces_available": r.spaces_available,
             "free_spaces": r.free_spaces, "opening_times": r.opening_times,
             "height_restriction": r.height_restriction, "prices_rates": r.prices_rates,
             "latitude": r.latitude, "longitude": r.longitude} for r in records]
    return jsonify(data), 200

# Get parking record by ID
# curl -X GET http://127.0.0.1:5000/api/parking/1
@app.route('/api/parking/<int:idd>', methods=['GET'])
def get_parking_by_id(idd):
    record = parking_dao.fetch_by_id(idd)
    if not record:
        return jsonify({"error": "Parking record not found"}), 404
    return jsonify({"idd": record.idd, "parking_name": record.parking_name,
                    "spaces_available": record.spaces_available, "free_spaces": record.free_spaces,
                    "opening_times": record.opening_times, "height_restriction": record.height_restriction,
                    "prices_rates": record.prices_rates, "latitude": record.latitude,
                    "longitude": record.longitude}), 200

# Create a new parking record
# curl -X DELETE http://127.0.0.1:5000/api/parking/101
@app.route('/api/parking', methods=['POST'])
def create_parking():
    try:
        data = request.json
        parking = Parking(**data)
        parking_dao.add(parking)
        return jsonify({"message": "Parking record created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Update a parking record
# curl -X DELETE http://127.0.0.1:5000/api/parking/101
@app.route('/api/parking/<int:idd>', methods=['PUT'])
def update_parking(idd):
    try:
        data = request.json
        parking = parking_dao.update(idd, data)
        if not parking:
            return jsonify({"error": "Parking record not found"}), 404
        return jsonify({"message": "Parking record updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Delete a parking record
# curl -X DELETE http://127.0.0.1:5000/api/parking/101
@app.route('/api/parking/<int:idd>', methods=['DELETE'])
def delete_parking(idd):
    try:
        parking = parking_dao.delete(idd)
        if not parking:
            return jsonify({"error": "Parking record not found"}), 404
        return jsonify({"message": "Parking record deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
