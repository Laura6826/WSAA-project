# WSAA-project: Web Services and Applications.
# DAO (Data Access Object) for the car park height restriction data.
# Author: Laura Lyons

import logging
import pymysql
from pymysql.err import MySQLError
import dbconfig as cfg

logging.basicConfig(level=logging.ERROR)

class CarParksDAO:
    """ Data Access Object for car park details. """
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
            print("Connected to MySQL in CarParksDAO with PyMySQL!")
        except MySQLError as err:
            print("Error connecting to MySQL in CarParksDAO:", err)
            raise

    def execute_query(self, sql, params=None, fetch=False, fetch_one=False):
        """ Executes a SQL query and returns the result. """
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
        """ Closes the database connection. """
        try:
            if self.connection and self.connection.open:
                self.connection.close()
                print("Database connection closed.")
        except MySQLError as err:
            logging.error("Error closing connection: %s", err) 

    def get_height_restriction(self, car_park_id):
        """Retrieves the height restriction for a specific car park."""
        sql = "SELECT height FROM carparkdetails WHERE id = %s"
        return self.execute_query(sql, (car_park_id,), fetch_one=True)

    def create_car_park(self, name, height):
        """Creates a new car park with the given name and height restriction."""
        with self.connection.cursor() as cursor:
            # ✅ Check if a car park with this name already exists
            cursor.execute("SELECT COUNT(*) FROM carparkdetails WHERE name = %s", (name,))
            existing_count = cursor.fetchone()["COUNT(*)"]

            if existing_count > 0:
                return None  # ✅ Prevent duplicate insertion

            # ✅ If not found, insert the new car park
            sql = "INSERT INTO carparkdetails (name, height) VALUES (%s, %s)"
            cursor.execute(sql, (name, height))
            self.connection.commit()
            new_id = cursor.lastrowid
        return new_id

    def get_all_car_parks(self):
        """Retrieves all car parks."""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM carparkdetails")
            result = cursor.fetchall()
        return result

    def get_car_park_by_id(self, car_park_id):
        """Retrieves a car park by ID."""
         # Check if the car park exists before attempting to retrieve
        sql = "SELECT * FROM carparkdetails WHERE id = %s"
        return self.execute_query(sql, (car_park_id,), fetch_one=True)

    def delete_car_park(self, car_park_id):
        """Deletes a car park by ID."""
         # Check if the car park exists before attempting to delete
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM carparkdetails WHERE id = %s"
            cursor.execute(sql, (car_park_id,))
            self.connection.commit()
            affected = cursor.rowcount
        return affected > 0
    
    def update_car_park_opening_hours_and_height(self, car_park_id, new_hours, new_height):
        """
        Updates:
        - The height restriction in carparkdetails.
        - The opening and closing times (and status) for each day in openinghourstable.
        
        new_hours should be a dict structured like:
        {
            "Monday":   {"open": "06:00", "close": "22:00"},
            "Tuesday":  {"open": "06:00", "close": "22:00"},
            ...
        }
        
        If either "open" or "close" is empty for a day, we treat that day as closed.
        """
        try:
            with self.connection.cursor() as cursor:
                # Update the height restriction in carparkdetails.
                sql_update_details = "UPDATE carparkdetails SET height = %s WHERE id = %s"
                cursor.execute(sql_update_details, (new_height, car_park_id))
                
                # Loop through each day to update opening hours.
                for day, times in new_hours.items():
                    # Determine status and times:
                    if times.get("open", "") == "" or times.get("close", "") == "":
                        status = "closed"
                        opening_time = None
                        closing_time = None
                    else:
                        status = "open"
                        opening_time = times.get("open")
                        closing_time = times.get("close")
                    
                    sql_update_hours = """
                        UPDATE openinghourstable
                        SET opening_time = %s, closing_time = %s, status = %s
                        WHERE car_park_id = %s AND day_of_week = %s
                    """
                    cursor.execute(sql_update_hours, 
                        (opening_time, closing_time, status, car_park_id, day))
                
                self.connection.commit()
                return True
        except Exception as e:
            logging.error("Error updating car park: %s", e)
            return False



    
    def __del__(self):
        try:
            if self.connection and self.connection.open:
                self.connection.close()
        except MySQLError as err:
            logging.error("Error during cleanup: %s", err)

