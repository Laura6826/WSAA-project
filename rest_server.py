# WSAA-project: Web Services and Applications.
# Main Flask application
# Author: Laura Lyons

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# External API details
API_URL = "	https://data.corkcity.ie/en_GB/api/3/action/datastore_search"
RESOURCE_ID = "c609d229-f7fe-4da9-a065-1e44f65bc7dc"

# Check if the API is reachable; http://127.0.0.1:5000/
@app.route('/')
def index():
    return "Welcome to the Parking API!"

# Fetch all records (Read)
# curl -X GET http://127.0.0.1:5000/api/fetch
@app.route('/api/fetch', methods=['GET'])
def fetch_parking_data():
    sql_query = f"""
    SELECT idd, name AS parking_name, spaces AS spaces_available, free_spaces,
    height_restrictions AS height_restriction
    FROM "{RESOURCE_ID}"
    """
    try:
        response = requests.get(API_URL, params={"sql": sql_query})
        if response.status_code == 200:
            data = response.json()
            records = data.get("result", {}).get("records", [])
            return jsonify(records), 200
        else:
            return jsonify({"error": f"Failed to fetch data. HTTP Status Code: {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Fetch a single record by ID (Read)
# curl -X GET http://127.0.0.1:5000/api/parking/1
@app.route('/api/parking/<int:idd>', methods=['GET'])
def fetch_parking_by_id(idd):
    sql_query = f"""
    SELECT idd, name AS parking_name, spaces AS spaces_available, free_spaces, opening_times,
    height_restrictions AS height_restriction, price AS prices_rates, latitude, longitude
    FROM "{RESOURCE_ID}" WHERE idd = {idd}
    """
    try:
        response = requests.get(API_URL, params={"sql": sql_query})
        if response.status_code == 200:
            data = response.json()
            record = data.get("result", {}).get("records", [])
            if not record:
                return jsonify({"error": "Parking record not found"}), 404
            return jsonify(record[0]), 200
        else:
            return jsonify({"error": f"Failed to fetch data. HTTP Status Code: {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Create a new parking record (Create)
# curl -X POST -H "Content-Type: application/json" -d '{"name": "New Parking", "spaces_available": 50}' http://127.0.0.1:5000/api/parking
@app.route('/api/parking', methods=['POST'])
def create_parking():
    # Simulating creation since the external API is read-only
    try:
        data = request.json
        return jsonify({"message": "Creation is not supported in external API. Simulated record:", "data": data}), 201
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Update a parking record (Update)
# curl -X DELETE http://127.0.0.1:5000/api/parking/1
@app.route('/api/parking/<int:idd>', methods=['PUT'])
def update_parking(idd):
    # Simulating update since the external API is read-only
    try:
        data = request.json
        data['idd'] = idd
        return jsonify({"message": "Update is not supported in external API. Simulated update:", "data": data}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Delete a parking record (Delete)
# # curl -X DELETE http://127.0.0.1:5000/api/parking/1
@app.route('/api/parking/<int:idd>', methods=['DELETE'])
def delete_parking(idd):
    # Simulating deletion since the external API is read-only
    try:
        return jsonify({"message": f"Deletion is not supported in external API. Simulated deletion of ID: {idd}"}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)


