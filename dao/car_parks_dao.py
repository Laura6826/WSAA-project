# WSAA-project: Web Services and Applications.
# DAO (Data Access Object) for the car park height restriction data.
# Author: Laura Lyons

import logging
import pymysql
from pymysql.err import MySQLError
import dbconfig as cfg

logging.basicConfig(level=logging.ERROR)

class CarParksDAO:
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
        try:
            if self.connection and self.connection.open:
                self.connection.close()
                print("Database connection closed.")
        except MySQLError as err:
            logging.error("Error closing connection: %s", err) 

    def get_height_restriction(self, car_park_id):
        sql = "SELECT height FROM carparkdetails WHERE id = %s" 
        return self.execute_query(sql, (car_park_id,), fetch_one=True)


    def create_car_park(self, name, height):
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO carparkdetails (name, height) VALUES (%s, %s)"
            cursor.execute(sql, (name, height))
            self.connection.commit()
            new_id = cursor.lastrowid
        return new_id

    def get_all_car_parks(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM carparkdetails")
            result = cursor.fetchall()
        return result

    def get_car_park_by_id(self, car_park_id):
        sql = "SELECT * FROM carparkdetails WHERE id = %s"
        return self.execute_query(sql, (car_park_id,), fetch_one=True)


    def update_car_park(self, car_park_id, name, height):
        with self.connection.cursor() as cursor:
            sql = "UPDATE carparkdetails SET name = %s, height = %s WHERE id = %s"
            cursor.execute(sql, (name, height, car_park_id))
            self.connection.commit()
            affected = cursor.rowcount
        return affected > 0

    def delete_car_park(self, car_park_id):
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM carparkdetails WHERE id = %s"
            cursor.execute(sql, (car_park_id,))
            self.connection.commit()
            affected = cursor.rowcount
        return affected > 0
    
    def __del__(self):
        try:
            if self.connection and self.connection.open:
                self.connection.close()
        except MySQLError as err:
            logging.error("Error during cleanup: %s", err)

