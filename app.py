# WSAA-project: Web Services and Applications.
# Main Flask application
# Author: Laura Lyons

# Create the Database and the Tables

from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///air_quality.db'
db = SQLAlchemy(app)

class EmissionPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(100), nullable=False)
    coordinates = db.Column(db.String(100), nullable=False)
    emission_type = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Float, nullable=False)

class AirQuality(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    pm25 = db.Column(db.Float, nullable=True)
    pm10 = db.Column(db.Float, nullable=True)
    co2 = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.String(100), nullable=False)
