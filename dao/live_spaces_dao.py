# WSAA-project: Web Services and Applications.
# DAO (Data Access Object) for Parking data.
# Author: Laura Lyons

import requests

API_URL = "https://data.corkcity.ie/en_GB/api/3/action/datastore_search_sql"
RESOURCE_ID = "f4677dac-bb30-412e-95a8-d3c22134e3c0"

class LiveSpacesDAO:
    def fetch_live_spaces(self):
        try:
            query = f"SELECT * FROM \"{RESOURCE_ID}\""
            response = requests.get(API_URL, params={"sql": query})
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            return data["result"]["records"]
        except Exception as e:
            print(f"Error fetching live spaces: {e}")
            return None

