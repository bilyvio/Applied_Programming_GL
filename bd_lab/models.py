import simplejson
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Serialise(object):
    def _asdict(self):
        result = simplejson.OrderedDict()
        for key in self.__mapper__.c.keys():
            if isinstance(getattr(self, key), datetime):
                result["x"] = getattr(self, key).timestamp() * 1000
                result["timestamp"] = result["x"]
            else:
                result[key] = getattr(self, key)

        return result


class Category(Base, Serialise):
    __tablename__ = "category"

    uid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    homePage = Column(String)


class Announcement(Base, Serialise):
    __tablename__ = "announcement"

    def __init__(self, name, releaseDate, local, location):
        self.name = name
        self.releaseDate = releaseDate
        self.local = local
        self.location = location

    def __init__(self, uid, name, releaseDate, location):
        self.uid = uid
        self.name = name
        self.releaseDate = releaseDate
        self.location = location

    uid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    releaseDate = Column(String)
    local = Column(Boolean)
    location = Column(String)
    manufacturer_uid = Column(Integer, ForeignKey(Category.uid))


class User(Base, Serialise):
    __tablename__ = "users"

    def __init__(self, name, location, username, password):
        self.name = name
        self.location = location
        self.username = username
        self.password = password

    uid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    location = Column(String)
    username = Column(String)
    password = Column(String)
