from marshmallow import validate, Schema, fields, post_load

from models import Announcement


class User(Schema):
    uid = fields.Integer()
    name = fields.String()
    location = fields.String()
    username = fields.String()
    password = fields.String()



class Announcement_Schema(Schema):
    uid = fields.Integer()
    name = fields.String()
    releaseDate = fields.String()
    local = fields.Boolean()
    location = fields.String()
    manufacturer_uid = fields.Integer()

    @post_load
    def make_announcement(self, data, **kwargs):
        return Announcement(**data)

