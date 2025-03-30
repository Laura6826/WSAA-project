# WSAA-project: Web Services and Applications.
# Main Flask application
# Author: Laura Lyons

from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Air Quality Interface!"

# Get all emissions records
# curl http://127.0.0.1:5000/emissions
@app.route('/emissions', methods=['GET'])
def get_all_emissions():
    return "Retrieve all emissions records"

# Find an emissions record by id
# curl http://127.0.0.1:5000/emissions/1
@app.route('/emissions/<int:id>', methods=['GET'])
def find_emission_by_id(id):
    return f"Retrieve emission record with ID: {id}"

# Create a new emissions record
# curl -X POST -d "{\"location\":\"test location\", \"pollutant\":\"CO2\", \"amount\":123.45}" -H "Content-Type: application/json" http://127.0.0.1:5000/emissions
@app.route('/emissions', methods=['POST'])
def create_emission():
    # Read JSON data from the request body
    json_data = request.json
    return f"Create new emission record: {json_data}"

# Update an emissions record
# curl -X PUT -d "{\"location\":\"updated location\", \"pollutant\":\"CO2\", \"amount\":456.78}" -H "Content-Type: application/json" http://127.0.0.1:5000/emissions/1
@app.route('/emissions/<int:id>', methods=['PUT'])
def update_emission(id):
    json_data = request.json
    return f"Update emission record {id}: {json_data}"

# Delete an emissions record
# curl -X DELETE http://127.0.0.1:5000/emissions/1
@app.route('/emissions/<int:id>', methods=['DELETE'])
def delete_emission(id):
    return f"Delete emission record with ID: {id}"

if __name__ == "__main__":
    app.run(debug=True)
