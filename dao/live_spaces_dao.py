# WSAA-project: Web Services and Applications.
# DAO (Data Access Object) for Parking data.
# Author: Laura Lyons

import logging
import requests

API_URL = "https://data.corkcity.ie/en_GB/api/3/action/datastore_search_sql"
RESOURCE_ID = "f4677dac-bb30-412e-95a8-d3c22134e3c0"

logging.basicConfig(level=logging.DEBUG)

class LiveSpacesDAO:
    def fetch_live_spaces(self):
        try:
            query = f'SELECT * FROM "{RESOURCE_ID}"'
            response = requests.get(API_URL, params={"sql": query}, timeout=10)
            response.raise_for_status()

            data = response.json()
            logging.debug("🔍 Live parking data: %s", data)

            return data.get("result", {}).get("records", [])
        except requests.exceptions.RequestException as e:
            logging.error("❌ Error fetching live spaces: %s", e)
            return []

