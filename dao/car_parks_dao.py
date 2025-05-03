# WSAA-project: Web Services and Applications.
# DAO (Data Access Object) for the car park height restriction data.
# Author: Laura Lyons

import logging
from mysql.connector import connect, Error
import dbconfig as cfg

logging.basicConfig(level=logging.ERROR)

class CarParksDAO:
    """DAO for managing car park records in the database."""

    def test_db_connection(self):
        """Tests database connection and logs potential credential errors."""
        try:
            logging.debug("Attempting to connect to the database...")
            with connect(
                host=cfg.mysql["host"],
                user=cfg.mysql["user"],
                password=cfg.mysql["password"],
                database=cfg.mysql["database"],
                port=cfg.mysql.get("port", 3306),
            ) as connection:
                logging.debug("✅ Database connection successful.")
                return True
        except Error as e:
            logging.error("❌ Database connection failed: %s", e)
            logging.error("🔍 Check credentials: host=%s, user=%s, database=%s, port=%s",
                          cfg.mysql["host"], cfg.mysql["user"], cfg.mysql["database"], cfg.mysql.get("port", 3306))
            return False

    def execute_query(self, sql, params=None, fetch=False):
        """Executes an SQL query with a managed connection."""
        try:
            with connect(
                host=cfg.mysql["host"],
                user=cfg.mysql["user"],
                password=cfg.mysql["password"],
                database=cfg.mysql["database"],
                port=cfg.mysql.get("port", 3306),
            ) as connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute(sql, params or ())
                    if fetch:
                        return cursor.fetchall()
                    connection.commit()
                    return True
        except Error as e:
            logging.error("❌ Query execution failed: %s", e)
            return False if not fetch else None

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
