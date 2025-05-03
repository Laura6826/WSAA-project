# WSAA-project: Web Services and Applications.
# DAO (Data Access Object) for the car park opening hours data.
# Author: Laura Lyons

import logging
import mysql
from mysql.connector import connect
import dbconfig as cfg

logging.basicConfig(level=logging.ERROR)

class OpeningHoursDAO:
    # DAO for managing opening hours in the database.

    def execute_query(self, sql, params=None, fetch=False):
        """
        Executes an SQL query within a managed MySQL connection.

        Args:
            sql (str): The SQL query to be executed.
            params (tuple, optional): Query parameters for the SQL execution. Defaults to None.
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
        except mysql.connector.Error as e:
            logging.error("Database error: %s", e)
            return False if not fetch else None

    def add_opening_hours(self, car_park_id, day, opening_time, closing_time, status):
        """
        Adds new opening hours for a car park.

        Args:
            car_park_id (int): ID of the car park.
            day (str): Day of the week.
            opening_time (str): Opening time (HH:MM format).
            closing_time (str): Closing time (HH:MM format).
            status (str): Status (e.g., Open/Closed).

        Returns:
            bool: True if added successfully, False otherwise.
        """
        sql = """
            INSERT INTO OpeningHours (car_park_id, day, opening_time, closing_time, status)
            VALUES (%s, %s, %s, %s, %s)
        """
        return self.execute_query(sql, (car_park_id, day, opening_time, closing_time, status))

    def get_opening_hours_for_car_park(self, car_park_id):
        """
        Retrieves opening hours for a specific car park.

        Args:
            car_park_id (int): ID of the car park.

        Returns:
            list | None: List of opening hours or None if an error occurs.
        """
        sql = "SELECT * FROM OpeningHours WHERE car_park_id = %s"
        return self.execute_query(sql, (car_park_id,), fetch=True)

    def update_opening_hours(self, opening_hours_id, day, opening_time, closing_time, status):
        """
        Updates existing opening hours entry.

        Args:
            opening_hours_id (int): ID of the opening hours entry.
            day (str): Day of the week.
            opening_time (str): Updated opening time.
            closing_time (str): Updated closing time.
            status (str): Updated status.

        Returns:
            bool: True if updated successfully, False otherwise.
        """
        sql = """
            UPDATE OpeningHours
            SET day = %s, opening_time = %s, closing_time = %s, status = %s
            WHERE id = %s
        """
        return self.execute_query(sql, (day, opening_time, closing_time, status, opening_hours_id))

    def delete_opening_hours(self, opening_hours_id):
        """
        Deletes an opening hours entry by ID.

        Args:
            opening_hours_id (int): ID of the opening hours entry.

        Returns:
            bool: True if deleted successfully, False otherwise.
        """
        sql = "DELETE FROM OpeningHours WHERE id = %s"
        return self.execute_query(sql, (opening_hours_id,))

