from app import db
Base = db.Model
class Category(db.Model):
    __tablename__ = "category"

    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(30))
    homePage = db.Column(db.VARCHAR(30))


class Announcement(db.Model):
    __tablename__ = "announcement"

    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(30))
    releaseDate = db.Column(db.VARCHAR(30))
    local = db.Column(db.Integer)
    manufacturer_uid = db.Column(db.Integer,db.ForeignKey(Category.uid))
    manufacturer = db.relationship("Category")


class Users(db.Model):
    __tablename__ = "users"

    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(30))