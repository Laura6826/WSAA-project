# WSAA-project: Web Services and Applications.
# DAO (Data Access Object) for the car park opening hours data.
# Author: Laura Lyons

import logging
import pymysql
from pymysql.err import MySQLError
import dbconfig as cfg

logging.basicConfig(level=logging.ERROR)

class OpeningHoursDAO:
    def __init__(self):
        try:
            self.connection = pymysql.connect(
                host=cfg.mysql["host"],
                user=cfg.mysql["user"],
                password=cfg.mysql["password"],
                database=cfg.mysql["database"],
                port=cfg.mysql.get("port", 3306),
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Connected to MySQL in OpeningHoursDAO with PyMySQL!")
        except MySQLError as err:
            print("Error connecting to MySQL in CarParksDAO:", err)
            raise

    def execute_query(self, sql, params=None, fetch=False, fetch_one=False):
        """Executes a SQL query and returns the result."""
        if not self.connection or not self.connection.open:
            logging.error("No active database connection.")
            return None

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params or ())
                result = cursor.fetchone() if fetch_one else (cursor.fetchall() if fetch else None)
                self.connection.commit()
                return result if fetch or fetch_one else True
        except MySQLError as err:
            logging.error("Query execution failed: %s", err)
            return False if not fetch else None

    def close_connection(self):
        """Closes the database connection."""
        try:
            if self.connection and self.connection.open:
                self.connection.close()
                print("Database connection closed.")
        except MySQLError as err:
            logging.error("Error closing connection: %s", err)

    def get_all_opening_hours(self):
        """Retrieves opening hours for all car parks."""
        sql = "SELECT * FROM openinghours"
        return self.execute_query(sql, fetch=True)

    def add_opening_hours(self, car_park_id, day_of_week, opening_time, closing_time, status="active"):
        """Adds new opening hours for a car park."""
        sql = """
            INSERT INTO openinghours (car_park_id, day_of_week, opening_time, closing_time, status)
            VALUES (%s, %s, %s, %s, %s)
        """
        return self.execute_query(sql, (car_park_id, day_of_week, opening_time, closing_time, status))

    def get_opening_hours_for_car_park(self, car_park_id):
        """Retrieves opening hours for a specific car park."""
        sql = "SELECT * FROM openinghours WHERE car_park_id = %s"
        return self.execute_query(sql, (car_park_id,), fetch=True)

    def update_opening_hours(self, openinghours_id, day_of_week, opening_time, closing_time, status):
        """Updates opening hours for a specific entry."""
        sql = """
            UPDATE openinghours
            SET day = %s, opening_time = %s, closing_time = %s, status = %s
            WHERE id = %s
        """
        return self.execute_query(sql, (day_of_week, opening_time, closing_time, status, openinghours_id))

    def delete_opening_hours(self, openinghours_id):
        """Deletes an opening hours entry by ID."""
        sql = "DELETE FROM openinghours WHERE id = %s"
        return self.execute_query(sql, (openinghours_id,))

    def __del__(self):
        try:
            if self.connection and self.connection.open:
                self.connection.close()
        except MySQLError as err:
            logging.error("Error during cleanup: %s", err)  
    