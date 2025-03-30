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
class EmissionDAO:
    def __init__(self):
        # Create the emissions table if it doesn't exist
        Base.metadata.create_all(engine)

    def add_emission(self, facility_name, location, pollutant, amount, compliance_status):
        new_emission = Emission(
            facility_name=facility_name,
            location=location,
            pollutant=pollutant,
            amount=amount,
            compliance_status=compliance_status
        )
        session.add(new_emission)
        session.commit()
        return new_emission

    def get_all_emissions(self):
        return session.query(Emission).all()

    def get_emission_by_id(self, emission_id):
        return session.query(Emission).filter(Emission.id == emission_id).first()

    def update_emission(self, emission_id, **kwargs):
        emission = session.query(Emission).filter(Emission.id == emission_id).first()
        if emission:
            for key, value in kwargs.items():
                setattr(emission, key, value)
            session.commit()
            return emission
        return None

    def delete_emission(self, emission_id):
        emission = session.query(Emission).filter(Emission.id == emission_id).first()
        if emission:
            session.delete(emission)
            session.commit()
            return True
        return False
