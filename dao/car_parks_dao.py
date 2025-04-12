# WSAA-project: Web Services and Applications.
# DAO (Data Access Object) for the car park height restriction data.
# Author: Laura Lyons

import mysql.connector
import dbconfig as cfg

class CarParksDAO:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=cfg.mysql["host"],
            user=cfg.mysql["user"],
            password=cfg.mysql["password"],
            database=cfg.mysql["database"],
            port=cfg.mysql.get("port", 3306)  # Default port is 3306
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    # Create a new car park
    def create_car_park(self, name, height):
        try:
            self.connect()
            sql = "INSERT INTO CarParks (name, height) VALUES (%s, %s)"
            self.cursor.execute(sql, (name, height))
            self.connection.commit()
            self.close()
            return True  # Indicate success
        except Exception as e:
            print(f"Error creating car park: {e}")
            self.close()
            return False

    # Read all car parks
    def get_all_car_parks(self):
        try:
            self.connect()
            sql = "SELECT * FROM CarParks"
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            self.close()
            return results
        except Exception as e:
            print(f"Error fetching car parks: {e}")
            self.close()
            return None

    # Read a car park by ID
    def find_car_park_by_id(self, car_park_id):
        try:
            self.connect()
            sql = "SELECT * FROM CarParks WHERE id = %s"
            self.cursor.execute(sql, (car_park_id,))
            result = self.cursor.fetchone()
            self.close()
            return result
        except Exception as e:
            print(f"Error fetching car park by ID: {e}")
            self.close()
            return None

    # Update an existing car park
    def update_car_park(self, car_park_id, name, height):
        try:
            self.connect()
            sql = "UPDATE CarParks SET name = %s, height = %s WHERE id = %s"
            self.cursor.execute(sql, (name, height, car_park_id))
            self.connection.commit()
            self.close()
            return True  # Indicate success
        except Exception as e:
            print(f"Error updating car park: {e}")
            self.close()
            return False

    # Delete a car park by ID
    def delete_car_park(self, car_park_id):
        try:
            self.connect()
            sql = "DELETE FROM CarParks WHERE id = %s"
            self.cursor.execute(sql, (car_park_id,))
            self.connection.commit()
            self.close()
            return True  # Indicate success
        except Exception as e:
            print(f"Error deleting car park: {e}")
            self.close()
            return False

