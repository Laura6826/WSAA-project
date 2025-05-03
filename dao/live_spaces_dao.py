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
            query = "SELECT * FROM \"%s\"" % RESOURCE_ID  
            logging.debug("Fetching live parking spaces with query: %s", query)
            
            response = requests.get(API_URL, params={"sql": query}, timeout=10)  
            response.raise_for_status()
            data = response.json()

            logging.debug("Live parking data retrieved: %s", data["result"]["records"])
            return data["result"]["records"]

        except requests.exceptions.RequestException as e:
            logging.error("❌ Error fetching live spaces: %s", e)
            return None
        except Exception as e:
            logging.error("❌ Unexpected error in fetch_live_spaces: %s", e)
            return None


