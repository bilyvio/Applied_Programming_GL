from marshmallow import validate, Schema, fields, post_load

from models import Announcement, User


class User_Schema(Schema):
    name = fields.String()
    location = fields.String()
    username = fields.String()
    password = fields.String()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class Announcement_Schema(Schema):

    uid = fields.Integer()
    name = fields.String()
    releaseDate = fields.String()
    local = fields.Boolean()
    location = fields.String()

    @post_load
    def make_announcement(self, data, **kwargs):
        return Announcement(**data)


class Update_Announcement_Schema(Schema):
    uid = fields.Integer()
    name = fields.String()
    releaseDate = fields.String()
    location = fields.String()

    @post_load
    def make_announcement(self, data, **kwargs):
        return Announcement(**data)
