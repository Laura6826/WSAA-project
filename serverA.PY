from dao.car_parks_dao import CarParksDAO
from dao.opening_hours_dao import OpeningHoursDAO

import logging
import sys
import os
import requests
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from schema.schema import CarParkSchema, OpeningHoursSchema
from marshmallow import ValidationError

# Force Flask Debug Mode
os.environ["FLASK_DEBUG"] = "1"

# Initialize Flask app
app = Flask(__name__, static_folder='static')

# DAO instanc
car_parks_dao = CarParksDAO()
opening_hours_dao = OpeningHoursDAO()

# Ensuring logs print to terminal
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]  # Ensures logs print in the terminal
)

print("Flask is starting...") # Print message to indicate Flask is starting

API_URL = "https://data.corkcity.ie/en_GB/api/3/action/datastore_search_sql"
RESOURCE_ID = "f4677dac-bb30-412e-95a8-d3c22134e3c0"

# Root endpoint
# Check if the API is reachable; http://127.0.0.1:5000/

@app.route('/')
def index():
    """ Render the index page """
    logging.debug("Serving the Parking Checker HTML file.")
    return render_template('parking_checker2.html')

# Fetch live parking spaces **independently**
def fetch_live_spaces():
    """ Fetch live parking spaces from the API """
    try:
        query = f'SELECT * FROM "{RESOURCE_ID}"'
        response = requests.get(API_URL, params={"sql": query}, timeout=10)
        response.raise_for_status()

        data = response.json()
        # print("Raw API Response:", json.dumps(data, indent=2))

        live_data = data.get("result", {}).get("records", [])

        for item in live_data:
            item["id"] = item.get("_id", None)  # Fix ID reference

        return live_data if live_data else []

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching live spaces: {e}")
        return []

# Fetch all car parks from MySQL and match with live data
# curl -X GET http://127.0.0.1:5000/api/car-parks

@app.route('/api/car-parks', methods=['GET'])
def get_car_parks():
    """ Fetch all car parks from MySQL and match with live data """
    car_parks = car_parks_dao.get_all_car_parks()
    live_data = fetch_live_spaces()

    # print("MySQL Car Park IDs:", [str(park["id"]) for park in car_parks])  
    # print("Live API Car Park IDs:", [str(item.get("id")) for item in live_data])

    for park in car_parks:
        park_id = str(park["id"])
        matching_live_data = next((item for item in live_data if str(item.get("id")) == park_id), None)

        if matching_live_data:
            park["free_spaces"] = matching_live_data.get("free_spaces", "Unavailable")
            # print(f"✅ Found live data for {park['name']}: {park['free_spaces']}")
        else:
            park["free_spaces"] = "No live data available"
            # print(f"❌ No live data for {park['name']}")

    return jsonify(car_parks)

# Fetch live parking spaces for selected car park
# curl -X GET http://127.0.0.1:5000/api/car-parks/<int:car_park_id>

@app.route('/api/car-parks/<int:car_park_id>', methods=['GET'])
def get_car_park_availability(car_park_id):
    """ Fetch live parking spaces for a specific car park """
    live_data = fetch_live_spaces()
    
    # Find live data for selected car park using "_id"
    matching_live_data = next((item for item in live_data if str(item.get("_id")) == str(car_park_id)), None)

    if matching_live_data:
        return jsonify({"car_park_id": car_park_id, "free_spaces": matching_live_data.get("free_spaces", "Unavailable")})
    else:
        return jsonify({"car_park_id": car_park_id, "free_spaces": "No live data available"})

# Fetch all opening hours (for display)
# curl -X GET http://127.0.0.1:5000/api/opening-hours

@app.route('/api/opening-hours', methods=['GET'])
def get_all_opening_hours():
    """ Fetch all opening hours """
    opening_hours = opening_hours_dao.get_all_opening_hours()
    return jsonify(opening_hours)

# Fetch opening hours for selected car park
# curl -X GET http://127.0.0.1:5000/api/opening-hours/1

@app.route('/api/opening-hours/<int:car_park_id>', methods=['GET'])
def get_opening_hours(car_park_id):
    opening_hours = opening_hours_dao.get_opening_hours_for_car_park(car_park_id)

    if not opening_hours:
        return jsonify({"message": "No opening hours available."})

    today = datetime.today().strftime("%A")
    now = datetime.now().strftime("%H:%M:%S")  # ✅ Current time

    today_hours = next((entry for entry in opening_hours if entry["day_of_week"] == today), None)

    if today_hours:
        opening_time = str(today_hours["opening_time"]) if today_hours["opening_time"] else None
        closing_time = str(today_hours["closing_time"]) if today_hours["closing_time"] else None
        status = today_hours.get("status", "Open as usual")

        # ✅ If it's "Open 24 Hours" AND times are NULL, display special message
        if status == "24 Hours" and not opening_time and not closing_time:
            return jsonify({"message": "This car park is open 24 hours today"})

        # ✅ If opening/closing times exist, don't show status
        if opening_time and closing_time:
            return jsonify({"day": today_hours["day_of_week"], "opening_time": opening_time, "closing_time": closing_time})

        # ✅ Otherwise, return status + whatever time info exists
        return jsonify({
            "day": today_hours["day_of_week"],
            "opening_time": opening_time or "N/A",
            "closing_time": closing_time or "N/A",
            "status": status if status != "24 Hours" else None 
        })

    return jsonify({"message": f"No opening hours available for {today}."})



# Update opening hours for a car park
# 
@app.route('/api/opening-hours/<int:openinghours_id>', methods=['PUT'])
def update_opening_hours(openinghours_id):
    data = request.json
    success = opening_hours_dao.update_opening_hours(
        openinghours_id, data["day"], data["opening_time"], data["closing_time"], data["status"]
    )
    return jsonify({"message": "Opening hours updated."}) if success else jsonify({"message": "Update failed."})

# Start Flask Server
if __name__ == "__main__":
    logging.debug("Starting Flask server on http://127.0.0.1:5000")
    print("Starting Flask server on http://127.0.0.1:5000")
    app.run(debug=True, use_reloader=False)


