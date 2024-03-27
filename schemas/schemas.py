from apiflask import Schema, fields
from apiflask.fields import File, String

#- LOG ENTRY SCHEMA

class LogEntrySchema(Schema):
    datetime = String(required=True)
    user = fields.String(required=True)
    endpoint = fields.String(required=True)
    payload = fields.String(required=True)
    class Meta:
        fields = ('datetime', 'user', 'endpoint', 'payload')

class Image(Schema):
    image = File()

class ApiFileSchema(Schema):
    file = File()

