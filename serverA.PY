from dao.car_parks_dao import CarParksDAO
from dao.opening_hours_dao import OpeningHoursDAO

import logging
import sys
import os
import requests
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from pymysql.err import MySQLError

dao = CarParksDAO()
if dao.connection.open:
    print("✅ Successfully connected to MySQL through DAO!")
else:
    print("❌ Connection failed!")

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

# print("Flask is starting...") # Print message to indicate Flask is starting

API_URL = "https://data.corkcity.ie/en_GB/api/3/action/datastore_search_sql"
RESOURCE_ID = "f4677dac-bb30-412e-95a8-d3c22134e3c0"

# Root endpoint
# Check if the API is reachable; http://127.0.0.1:5000/

@app.route('/')
def index():
    """ Render the index page """
    logging.debug("Serving the Parking Checker HTML file.")
    return render_template('parking_checker2.html')

@app.route('/api/routes', methods=['GET'])
def list_routes():
    from flask import jsonify
    output = {rule.rule: list(rule.methods) for rule in app.url_map.iter_rules()}
    return jsonify(output)

# Fetch live parking spaces

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

# Fetch opening hours for selected car park
# curl -X GET http://127.0.0.1:5000/api/opening-hours/1

@app.route('/api/opening-hours/<int:car_park_id>', methods=['GET'])
def get_opening_hours(car_park_id):
    """ Fetch opening hours for a specific car park """
    opening_hours = opening_hours_dao.get_opening_hours_for_car_park(car_park_id)

    if not opening_hours:
        return jsonify({"message": "There is no data available for the opening hours car park."})

    today = datetime.today().strftime("%A")
    now = datetime.now().strftime("%H:%M")  # ✅ Current time

    today_hours = next((entry for entry in opening_hours if entry["day_of_week"] == today), None)

    if today_hours:
        opening_time = str(today_hours["opening_time"])[:-3] if today_hours["opening_time"] else None  # ✅ Removes seconds
        closing_time = str(today_hours["closing_time"])[:-3] if today_hours["closing_time"] else None  # ✅ Removes seconds
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


# Fetch height restrictions for all car parks (for display)
# curl -X GET http://127.0.0.1:5000/api/height-restrictions/1

@app.route('/api/height-restriction/<int:car_park_id>', methods=['GET'])
def get_height_restriction(car_park_id):
    restriction = car_parks_dao.get_height_restriction(car_park_id)

    print("🔍 Querying height restriction for Car Park ID:", car_park_id)
    print("🔍 Raw database result:", restriction)

    if restriction:
        height_value = float(restriction["height"])  # ✅ Extract only the numerical value
        formatted_height = f"{height_value:.2f}m"  # ✅ Ensure correct unit display

        print("✅ Formatted Height Restriction:", formatted_height)
        return jsonify({"height_restriction": formatted_height})  

    print("❌ No height restriction found for Car Park ID:", car_park_id)
    return jsonify({"message": "No height restriction available for this car park."})

# Add a car park
# curl -X POST http://

@app.route('/api/add-car-park', methods=['POST'])
def add_car_park():
    try:
        data = request.json
        name = data.get('name')
        height_restriction = data.get('height_restriction')
        opening_hours = data.get('opening_hours', {})

        new_id = car_parks_dao.create_car_park(name, height_restriction)

        print("🔍 Debugging: Opening Hours Received in Flask", opening_hours)  # ✅ Debugging

        if not name or name.strip() == "":
            return jsonify({"error": "Car park name cannot be empty"}), 400

        if not opening_hours:
            return jsonify({"error": "Opening hours data is missing!"}), 400

        # ✅ Loop through all days to add opening hours
        for day, times in opening_hours.items():
            if times and times[0] and times[1]:  # ✅ Ensure valid times
                opening_time, closing_time = times
                opening_hours_dao.add_opening_hours(new_id, day, opening_time, closing_time, "active")
                print(f"✅ Stored {day}: {opening_time} - {closing_time}")  # ✅ Log each entry stored

        return jsonify({"message": f"Car park '{name}' added with full weekly hours!", "car_park_id": new_id})

    except (KeyError, ValueError, TypeError) as e:  # Replace with specific exceptions
        print(f"❌ Server error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


# Add opening hours
@app.route('/api/add-opening-hours', methods=['POST'])
def add_opening_hours():
    """ Adds opening hours for a car park """
    data = request.json
    car_park_id = data.get('car_park_id')  # ✅ Links to car park ID
    opening_time = data.get('opening_time')
    closing_time = data.get('closing_time')
    is_24_hours = data.get('is_24_hours', False)

    sql = """
    INSERT INTO opening_hours (car_park_id, opening_time, closing_time, is_24_hours)
    VALUES (%s, %s, %s, %s)
    """
    
    execute_query(sql, (car_park_id, opening_time, closing_time, is_24_hours))
    
    return jsonify({"message": f"Opening hours added for Car Park ID {car_park_id}!"})

# Delete  a car park
@app.route('/delete_car_park', methods=['POST'])
def delete_car_park():
    """Deletes a car park and its associated opening hours with full error handling."""
    
    car_park_id = request.form.get('car_park_id')  # Extract car park ID from the request


    if not car_park_id or not car_park_id.isdigit():
        return jsonify({"message": "Invalid car park ID provided."}), 400

    # Check if car park exists before attempting deletion
    car_park_exists = car_parks_dao.get_car_park_by_id(car_park_id)

    if not car_park_exists:
        return jsonify({"message": "Error: Car park not found."}), 404

    try:
        with car_parks_dao.connection.cursor() as cursor:
            cursor.execute("START TRANSACTION")

            # Delete opening hours first
            cursor.execute("DELETE FROM openinghours WHERE car_park_id = %s", (car_park_id,))

            # Delete car park
            cursor.execute("DELETE FROM carparkdetails WHERE id = %s", (car_park_id,))
            
            cursor.execute("COMMIT")

        return jsonify({"message": "Car park and opening hours deleted successfully."}), 200

    except MySQLError as err:
        cursor.execute("ROLLBACK")  # Rollback in case of failure
        logging.error(f"Transaction Error: {err}")
        return jsonify({"message": "Database transaction failed. Car park was not deleted."}), 500

# Update a car park
@app.route('/update_car_park', methods=['POST'])
def update_car_park():
    data = request.json
    car_park_id = data.get('id')
    new_hours = data.get('opening_hours')
    new_height = data.get('height_restriction')
    
    # Check that the car park exists.
    car_park = car_parks_dao.get_car_park_by_id(car_park_id)
    if not car_park:
        return jsonify({"message": "❌ Error: Car park not found."}), 404

    success = car_parks_dao.update_car_park_opening_hours_and_height(car_park_id, new_hours, new_height)
    if success:
        return jsonify({"message": "✅ Car park updated successfully."}), 200
    else:
        return jsonify({"message": "❌ Error updating car park."}), 500


    
# Start Flask Server
if __name__ == "__main__":
    logging.debug("Starting Flask server on http://127.0.0.1:5000")
    print("Starting Flask server on http://127.0.0.1:5000")
    app.run(debug=True, use_reloader=False)