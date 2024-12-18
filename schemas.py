from marshmallow import Schema, fields

# User Schema
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

# Account Schema
class AccountSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    balance = fields.Float(dump_only=True)

# Record Schema
class RecordSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    amount = fields.Float(required=True)
    timestamp = fields.DateTime(dump_only=True)
