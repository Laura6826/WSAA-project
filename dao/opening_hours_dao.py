# WSAA-project: Web Services and Applications.
# DAO (Data Access Object) for the car park opening hours data.
# Author: Laura Lyons

import mysql.connector
import dbconfig as cfg

class OpeningHoursDAO:
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

    # Create new opening hours entry
    def add_opening_hours(self, car_park_id, day, opening_time, closing_time, status):
        try:
            self.connect()
            sql = """
                INSERT INTO OpeningHours (car_park_id, day, opening_time, closing_time, status)
                VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(sql, (car_park_id, day, opening_time, closing_time, status))
            self.connection.commit()
            self.close()
            return True  # Indicate success
        except Exception as e:
            print(f"Error adding opening hours: {e}")
            self.close()
            return False

    # Read all opening hours for a specific car park
    def get_opening_hours_for_car_park(self, car_park_id):
        try:
            self.connect()
            sql = "SELECT * FROM OpeningHours WHERE car_park_id = %s"
            self.cursor.execute(sql, (car_park_id,))
            results = self.cursor.fetchall()
            self.close()
            return results
        except Exception as e:
            print(f"Error fetching opening hours: {e}")
            self.close()
            return None

    # Update existing opening hours entry
    def update_opening_hours(self, opening_hours_id, day, opening_time, closing_time, status):
        try:
            self.connect()
            sql = """
                UPDATE OpeningHours
                SET day = %s, opening_time = %s, closing_time = %s, status = %s
                WHERE id = %s
            """
            self.cursor.execute(sql, (day, opening_time, closing_time, status, opening_hours_id))
            self.connection.commit()
            self.close()
            return True  # Indicate success
        except Exception as e:
            print(f"Error updating opening hours: {e}")
            self.close()
            return False

    # Delete opening hours entry by ID
    def delete_opening_hours(self, opening_hours_id):
        try:
            self.connect()
            sql = "DELETE FROM OpeningHours WHERE id = %s"
            self.cursor.execute(sql, (opening_hours_id,))
            self.connection.commit()
            self.close()
            return True  # Indicate success
        except Exception as e:
            print(f"Error deleting opening hours: {e}")
            self.close()
            return False

