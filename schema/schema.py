# This module handles car park data validation and API requests. 
# It includes schemas for data validation using Marshmallow. 
# Reference = https://marshmallow.readthedocs.io/en/latest/, recommended via AI.

from marshmallow import Schema, fields, validate, post_load

class OpeningHoursSchema(Schema):
    day = fields.Str(required=True)
    opening_time = fields.Str(required=True, 
                              validate=validate.Regexp(r"^([0-1]\d|2[0-3]):([0-5]\d)$"))
    closing_time = fields.Str(required=True, 
                              validate=validate.Regexp(r"^([0-1]\d|2[0-3]):([0-5]\d)$"))
    status = fields.Str(required=False)

    @post_load
    def set_default_status(self, data, **kwargs):
        if "status" not in data:
            data["status"] = "Open"
        return data

    class Meta:
        pass  # Meta class can be used for additional options if needed

class CarParkSchema(Schema):
    name = fields.Str(required=True)
    height = fields.Float(required=True)
    opening_hours = fields.List(
        fields.Nested(OpeningHoursSchema),
        required=True, 
        validate=validate.Length(min=1)  # Ensure at least one opening hours entry
    )

