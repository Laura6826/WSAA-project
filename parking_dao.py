# WSAA-project: Web Services and Applications.
# REST-SERVER for car-park space availaibility in Cork City.
# Author: Laura Lyons

from db_setup import Session, Parking


# DAO (Data Access Object) for Parking
class ParkingDAO:
    def __init__(self):
        self.session = Session()

    def fetch_all(self):
        return self.session.query(Parking).all()

    def fetch_by_id(self, idd):
        return self.session.query(Parking).filter_by(idd=idd).first()

    def add(self, parking):
        self.session.add(parking)
        self.session.commit()

    def update(self, idd, updated_data):
        parking = self.fetch_by_id(idd)
        if parking:
            for key, value in updated_data.items():
                setattr(parking, key, value)
            self.session.commit()
        return parking

    def delete(self, idd):
        parking = self.fetch_by_id(idd)
        if parking:
            self.session.delete(parking)
            self.session.commit()
        return parking
