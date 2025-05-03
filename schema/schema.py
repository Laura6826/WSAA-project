"""
This module handles car park data validation and API requests.
It includes schemas for data validation using Marshmallow.
Reference: https://marshmallow.readthedocs.io/en/latest/
"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate, post_load
from models.car_park import CarPark 
from models.opening_hours import OpeningHours  

class OpeningHoursSchema(SQLAlchemyAutoSchema):
    """Schema for car park opening hours."""
    class Meta:
        model = OpeningHours
        load_instance = True

    day = fields.Str(required=True)
    opening_time = fields.Str(
        required=True,
        validate=validate.Regexp(r"^([0-1]\d|2[0-3]):([0-5]\d)$"))
    closing_time = fields.Str(
        required=True,
        validate=validate.Regexp(r"^([0-1]\d|2[0-3]):([0-5]\d)$"))
    status = fields.Str(required=False)

    @post_load
    def set_default_status(self, data, **kwargs):
        if "status" not in data:
            data["status"] = "Open"
        return data


class CarParkSchema(SQLAlchemyAutoSchema):
    """Schema for car park records."""
    class Meta:
        model = CarPark
        load_instance = True

    name = fields.Str(required=True)
    height = fields.Float(required=True)
    opening_hours = fields.List(
        fields.Nested(OpeningHoursSchema),
        required=True,
        validate=validate.Length(min=1)  # Ensure at least one entry
    )
