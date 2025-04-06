# WSAA-project: Web Services and Applications.
# Database set up for the Cork City carpark availability.
# Author: Laura Lyons

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine('sqlite:///parking.db')  # SQLite database
Session = sessionmaker(bind=engine)

# Parking model
class Parking(Base):
    __tablename__ = 'parking'
    idd = Column(Integer, primary_key=True)  # Unique identifier
    parking_name = Column(String(100), nullable=False)  # Parking lot name
    spaces_available = Column(Integer, nullable=False)  # Total spaces
    free_spaces = Column(Integer, nullable=False)  # Available free spaces
    opening_times = Column(String(100), nullable=False)  # Opening hours
    height_restriction = Column(String(100), nullable=True)  # Maximum height restriction
    prices_rates = Column(String(100), nullable=True)  # Pricing rates
    latitude = Column(Float, nullable=False)  # Geographic latitude
    longitude = Column(Float, nullable=False)  # Geographic longitude

# Function to initialize the database
def init_db():
    """
    Initializes the database and creates tables if they don't already exist.
    """
    try:
        Base.metadata.create_all(engine)
        print("Database initialized and tables created (if not already present).")
    except Exception as e:
        print(f"An error occurred during database initialization: {str(e)}")

