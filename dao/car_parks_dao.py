# WSAA-project: Web Services and Applications.
# DAO (Data Access Object) for the car park height restriction data.
# Author: Laura Lyons

import logging
from mysql.connector import connect, Error
import dbconfig as cfg

logging.basicConfig(level=logging.ERROR)

class CarParksDAO:
    """DAO for managing car park records in the 'carparks' database."""

    def __init__(self):
        """Initialize database connection when DAO object is created."""
        try:
            self.connection = connect(
                host=cfg.mysql["host"],
                user=cfg.mysql["user"],
                password=cfg.mysql["password"],
                database="carparks",
                port=cfg.mysql.get("port", 3306),
            )
            print("✅ CarParksDAO initialized successfully!")
        except Error as e:
            logging.error("❌ Database connection failed: %s", e)
            self.connection = None  # Prevent further errors

    def execute_query(self, sql, params=None, fetch=False):
        """Executes a SQL query using the existing connection."""
        if not self.connection:
            logging.error("❌ No database connection available.")
            return None
        
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(sql, params or ())
                if fetch:
                    return cursor.fetchall()
                self.connection.commit()
                return True
        except Error as e:
            logging.error("❌ Query execution failed: %s", e)
            return False if not fetch else None

    def close_connection(self):
        """Closes the database connection when done."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔴 Database connection closed.")

    def create_car_park(self, name, height):
        """Creates a new car park."""
        sql = "INSERT INTO carparkdetails (name, height) VALUES (%s, %s)"
        return self.execute_query(sql, (name, height))

    def get_all_car_parks(self):
        """Retrieves all car parks."""
        sql = "SELECT * FROM carparkdetails"
        return self.execute_query(sql, fetch=True)

    def get_car_park_by_id(self, car_park_id):
        """Retrieves a car park by ID."""
        sql = "SELECT * FROM carparkdetails WHERE id = %s"
        return self.execute_query(sql, (car_park_id,), fetch=True)

    def update_car_park(self, car_park_id, name, height):
        """Updates an existing car park."""
        sql = "UPDATE carparkdetails SET name = %s, height = %s WHERE id = %s"
        return self.execute_query(sql, (name, height, car_park_id))

    def delete_car_park(self, car_park_id):
        """Deletes a car park by ID."""
        sql = "DELETE FROM carparkdetails WHERE id = %s"
        return self.execute_query(sql, (car_park_id,))

