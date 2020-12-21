from flask import Flask, request, jsonify
from marshmallow import ValidationError
from sqlalchemy import create_engine, Boolean
from sqlalchemy.orm import sessionmaker
from flask_httpauth import HTTPBasicAuth
import hashlib
from models import User, Announcement
from schemas import Announcement_Schema, User_Schema, Update_Announcement_Schema

engine = create_engine("postgresql://violetta:123456@localhost:5432/my_database")
Session = sessionmaker(bind=engine)
session = Session()

auth = HTTPBasicAuth()
app = Flask(__name__)


@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    name = data['name']
    location = data['location']
    username = data['username']
    password = data['password']
    if session.query(User).filter_by(username=username).first() is None:
        session.add(User(name, location, username, hashlib.md5(password.encode()).hexdigest()))
        session.commit()
        return 'successful operation', 200
    return 'Username is already in use', 404


@auth.verify_password
def verify_password(username, password):
    return session.query(User).filter_by(username=username,
                                                password=hashlib.md5(password.encode()).hexdigest()).first() is not None


@app.route('/user/<username>', methods=['GET'])
@auth.login_required
def get_user_by_username(username):
    user = session.query(User).filter_by(username=username).first()
    if user is not None:
        user.password = None
        return jsonify(user._asdict()), 200
    return 'User does not exist', 404


@app.route('/user', methods=['PUT'])
@auth.login_required
def update_user():
    try:
        data = request.get_json()
        name = data['name']
        location = data['location']
        user = session.query(User).filter_by(username=auth.current_user()).first()
        user.name = name
        user.location = location
        session.commit()
        return 'Successful operation', 200
    except ValidationError:
        return 'Invalid input', 404


@app.route('/user', methods=['DELETE'])
@auth.login_required
def delete_user():
    try:
        session.delete(session.query(User).filter_by(username=auth.current_user()).first())
        session.commit()
        return 'Successful operation', 200
    except ValidationError:
        return 'Invalid input', 404


@app.route('/add_announcement', methods=['POST'])
@auth.login_required
def add_announcement():
    try:
        user = session.query(User).filter_by(username=auth.current_user()).first()
        announcement = Announcement_Schema().load(request.json)
        announcement.manufacturer_uid = user.uid
        session.add(announcement)
        session.commit()
        return 'Successful operation', 200
    except ValidationError as error:
        print(error)
        return 'Invalid input', 404


@app.route('/announcement/<uid>', methods=['GET'])
@auth.login_required
def get_announcement_by_id(uid):
    announcement = session.query(Announcement).filter_by(uid=int(uid)).first()
    if announcement is not None:
        return Announcement_Schema().dump(announcement), 200
    return 'Announcement does not exist', 404


@app.route('/announcement', methods=['PUT'])
@auth.login_required
def update_announcement_by_id():
    try:
        user = session.query(User).filter_by(username=auth.current_user()).first()
        announcement = Update_Announcement_Schema().load(request.json)
        announcement_up = session.query(Announcement).filter_by(uid=int(announcement.uid)).first()
        if announcement_up is None:
            return 'Announcement does not exist', 404
        if user.uid != announcement_up.manufacturer_uid:
            return 'Announcement does not belong to user', 409
        announcement_up.name = announcement.name
        announcement_up.releaseDate = announcement.releaseDate
        announcement_up.location = announcement.location
        session.commit()
        return 'Successful operation', 200
    except ValidationError:
        return 'Invalid input', 404


@app.route('/announcement/<uid>', methods=['DELETE'])
@auth.login_required
def delete_announcement_by_ud(uid):
    try:
        user = session.query(User).filter_by(username=auth.current_user()).first()
        announcement_up = session.query(Announcement).filter_by(uid=int(uid)).first()
        if announcement_up is None:
            return 'Announcement does not exist', 404
        if user.uid != announcement_up.manufacturer_uid:
            return 'Announcement does not belong to user', 409
        session.delete(announcement_up)
        session.commit()
        return 'Successful operation', 200
    except ValidationError:
        return 'Invalid input', 404


if __name__ == 'main':
    app.run()
