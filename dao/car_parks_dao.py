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
        self.connection = mysql.connector.connect(**cfg.mysql)
        self.cursor = self.connection.cursor(dictionary=True)

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def get_all_car_parks(self):
        try:
            self.connect()
            sql = "SELECT * FROM CarParks"
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            self.close()
            return results
        except Exception as e:
            print(f"Error: {e}")
            self.close()
            return None
