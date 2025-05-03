# WSAA-project: Web Services and Applications.
# DAO (Data Access Object) for the car park height restriction data.
# Author: Laura Lyons

import logging
from mysql.connector import connect, Error
import dbconfig as cfg

logging.basicConfig(level=logging.ERROR)

class CarParksDAO:
    """DAO for managing car park records in the database."""

    def execute_query(self, sql, params=None, fetch=False):
        """
        Executes an SQL query with a managed connection.

        Args:
            sql (str): SQL query to be executed.
            params (tuple, optional): Query parameters. Defaults to None.
            fetch (bool, optional): Whether to fetch results (True) or commit changes (False).

        Returns:
            list | bool: Query results if fetch=True, otherwise True/False indicating success.
        """
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
            logging.error("Database error: %s", e)
            return False if not fetch else None

    def create_car_park(self, name, height):
        """Creates a new car park."""
        sql = "INSERT INTO CarParks (name, height) VALUES (%s, %s)"
        return self.execute_query(sql, (name, height))

    def get_all_car_parks(self):
        """Retrieves all car parks."""
        sql = "SELECT * FROM CarParks"
        return self.execute_query(sql, fetch=True)

    def get_car_park_by_id(self, car_park_id):
        """Retrieves a car park by ID."""
        sql = "SELECT * FROM CarParks WHERE id = %s"
        return self.execute_query(sql, (car_park_id,), fetch=True)

    def update_car_park(self, car_park_id, name, height):
        """Updates an existing car park."""
        sql = "UPDATE CarParks SET name = %s, height = %s WHERE id = %s"
        return self.execute_query(sql, (name, height, car_park_id))

    def delete_car_park(self, car_park_id):
        """Deletes a car park by ID."""
        sql = "DELETE FROM CarParks WHERE id = %s"
        return self.execute_query(sql, (car_park_id,))

