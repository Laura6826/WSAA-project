# Reference = https://marshmallow.readthedocs.io/en/latest/, recommended via AI

from marshmallow import Schema, fields

class OpeningHoursSchema(Schema):
    day = fields.Str(required=True)
    opening_time = fields.Str(required=True)
    closing_time = fields.Str(required=True)
    status = fields.Str(required=False)

class CarParkSchema(Schema):
    name = fields.Str(required=True)
    height = fields.Float(required=True)
    opening_hours = fields.List(fields.Nested(OpeningHoursSchema), required=True)
