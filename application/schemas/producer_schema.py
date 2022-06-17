from marshmallow import Schema, fields


class ProducerSchema(Schema):
    producer = fields.Str(required=True)
    interval = fields.Int(required=True)
    previousWin = fields.Int(required=True)
    followingWin = fields.Int(required=True)
