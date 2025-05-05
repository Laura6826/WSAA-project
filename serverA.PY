from dao.car_parks_dao import CarParksDAO

import logging
import json
import sys
import requests
from flask import Flask, request, jsonify, render_template
from schema.schema import CarParkSchema, OpeningHoursSchema
from marshmallow import ValidationError

import os

# Force Flask Debug Mode
os.environ["FLASK_DEBUG"] = "1"

# Initialize Flask app
app = Flask(__name__, static_folder='static')

# DAO instance for MySQL car parks (Dropdown only)
car_parks_dao = CarParksDAO()

# Ensuring logs print to terminal
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]  # ✅ Ensures logs print in the terminal
)

print("🚀 Flask is starting...")  # ✅ Print test
logging.debug("✅ Flask logging is working!")  # ✅ Logging test

API_URL = "https://data.corkcity.ie/en_GB/api/3/action/datastore_search_sql"
RESOURCE_ID = "f4677dac-bb30-412e-95a8-d3c22134e3c0"

# Root endpoint
# Check if the API is reachable; http://127.0.0.1:5000/

@app.route('/')
def index():
    """ Render the index page """
    logging.debug("Serving the Parking Checker HTML file.")
    return render_template('parking_checker2.html')

# ✅ Fetch live parking spaces **independently**
def fetch_live_spaces():
    """ Fetch live parking spaces from the API """
    try:
        query = f'SELECT * FROM "{RESOURCE_ID}"'
        response = requests.get(API_URL, params={"sql": query}, timeout=10)
        response.raise_for_status()

        data = response.json()
        # print("🔍 Raw API Response:", json.dumps(data, indent=2))  # ✅ Print full API response

        live_data = data.get("result", {}).get("records", [])

        # ✅ Force ID correction
        for item in live_data:
            item["id"] = item.get("_id", None)  # ✅ Fix ID reference

        return live_data if live_data else []

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching live spaces: {e}")
        return []


# ✅ Fix car park ID matching
@app.route('/api/car-parks', methods=['GET'])
def get_car_parks():
    """ Fetch all car parks from MySQL and match with live data """
    car_parks = car_parks_dao.get_all_car_parks()
    live_data = fetch_live_spaces()

    print("🔍 MySQL Car Park IDs:", [str(park["id"]) for park in car_parks])  
    print("🔍 Live API Car Park IDs:", [str(item.get("id")) for item in live_data])  # ✅ Fix ID reference

    for park in car_parks:
        park_id = str(park["id"])
        matching_live_data = next((item for item in live_data if str(item.get("id")) == park_id), None)

        if matching_live_data:
            park["free_spaces"] = matching_live_data.get("free_spaces", "Unavailable")
            print(f"✅ Found live data for {park['name']}: {park['free_spaces']}")
        else:
            park["free_spaces"] = "No live data available"
            print(f"❌ No live data for {park['name']}")

    return jsonify(car_parks)

# ✅ Fetch live parking spaces for selected car park
@app.route('/api/car-parks/<int:car_park_id>', methods=['GET'])
def get_car_park_availability(car_park_id):
    live_data = fetch_live_spaces()
    
    # Find live data for selected car park using "_id"
    matching_live_data = next((item for item in live_data if str(item.get("_id")) == str(car_park_id)), None)

    if matching_live_data:
        return jsonify({"car_park_id": car_park_id, "free_spaces": matching_live_data.get("free_spaces", "Unavailable")})
    else:
        return jsonify({"car_park_id": car_park_id, "free_spaces": "No live data available"})

# ✅ Start Flask Server
if __name__ == "__main__":
    logging.debug("🚀 Starting Flask server on http://127.0.0.1:5000")
    print("Starting Flask server on http://127.0.0.1:5000")
    app.run(debug=True, use_reloader=False)


