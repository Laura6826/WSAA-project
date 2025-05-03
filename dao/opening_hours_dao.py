# WSAA-project: Web Services and Applications.
# DAO (Data Access Object) for the car park opening hours data.
# Author: Laura Lyons

import logging
from mysql.connector import connect, Error  # Ensure proper error handling
import dbconfig as cfg

logging.basicConfig(level=logging.ERROR)

class OpeningHoursDAO:
    """DAO for managing opening hours in the database."""

    def execute_query(self, sql, params=None, fetch=False):
        """
        Executes an SQL query within a managed MySQL connection.

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

    def add_opening_hours(self, car_park_id, day, opening_time, closing_time, status):
        """Adds new opening hours for a car park."""
        sql = """
            INSERT INTO OpeningHours (car_park_id, day, opening_time, closing_time, status)
            VALUES (%s, %s, %s, %s, %s)
        """
        return self.execute_query(sql, (car_park_id, day, opening_time, closing_time, status))

    def get_opening_hours_for_car_park(self, car_park_id):
        """Retrieves opening hours for a specific car park."""
        sql = "SELECT * FROM OpeningHours WHERE car_park_id = %s"
        return self.execute_query(sql, (car_park_id,), fetch=True)

    def update_opening_hours(self, opening_hours_id, day, opening_time, closing_time, status):
        """Updates existing opening hours entry."""
        sql = """
            UPDATE OpeningHours
            SET day = %s, opening_time = %s, closing_time = %s, status = %s
            WHERE id = %s
        """
        return self.execute_query(sql, (day, opening_time, closing_time, status, opening_hours_id))

    def delete_opening_hours(self, opening_hours_id):
        """Deletes an opening hours entry by ID."""
        sql = "DELETE FROM OpeningHours WHERE id = %s"
        return self.execute_query(sql, (opening_hours_id,))
