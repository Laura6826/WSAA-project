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
        self.connection = mysql.connector.connect(**cfg.mysql)
        self.cursor = self.connection.cursor(dictionary=True)

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def get_opening_hours_for_car_park(self, car_park_id):
        try:
            self.connect()
            sql = "SELECT * FROM OpeningHours WHERE car_park_id = %s"
            self.cursor.execute(sql, (car_park_id,))
            results = self.cursor.fetchall()
            self.close()
            return results
        except Exception as e:
            print(f"Error: {e}")
            self.close()
            return None
