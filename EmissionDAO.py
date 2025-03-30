# WSAA-project: Web Services and Applications.
# DAO for Air Quality Emissions
# Author: Laura Lyons

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# SQLAlchemy base and engine
Base = declarative_base()
engine = create_engine('sqlite:///emissions.db')  # Replace with your database URI
Session = sessionmaker(bind=engine)
session = Session()

# Emission model
class Emission(Base):
    __tablename__ = 'emissions'

    id = Column(Integer, primary_key=True)
    facility_name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    pollutant = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    compliance_status = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

# DAO class
import sqlite3

class EmissionDAO:
    def __init__(self, db_path):
        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        # Connect to the database and create tables if they don't exist
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                pollutant TEXT CHECK (pollutant IN ('PM10', 'PM2.5', 'NOx', 'SOx')) NOT NULL,
                concentration REAL NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def add_emission(self, location, pollutant, concentration, timestamp):
        # Add an emission record
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO emissions (location, pollutant, concentration, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (location, pollutant, concentration, timestamp))
        conn.commit()
        conn.close()

    def get_emissions(self):
        # Retrieve all emissions
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM emissions')
        rows = cursor.fetchall()
        conn.close()
        return rows

    def update_emission(self, emission_id, location, pollutant, concentration, timestamp):
        # Update an emission record
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE emissions
            SET location = ?, pollutant = ?, concentration = ?, timestamp = ?
            WHERE id = ?
        ''', (location, pollutant, concentration, timestamp, emission_id))
        conn.commit()
        conn.close()

    def delete_emission(self, emission_id):
        # Delete an emission record
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM emissions WHERE id = ?', (emission_id,))
        conn.commit()
        conn.close()

# Example usage
if __name__ == '__main__':
    dao = EmissionDAO('emissions.db')
    dao.add_emission('Dublin', 'PM10', 25.5, '2025-03-30T14:00:00')
    emissions = dao.get_emissions()
    for emission in emissions:
        print(emission)

