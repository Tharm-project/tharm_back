from marshmallow import Schema, fields

class UserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    display_name = fields.Str()

class EmailSchema(Schema):
    email = fields.Email(required=True)
    query = fields.Str()
