from flask import Flask, request, jsonify
from marshmallow import ValidationError
from sqlalchemy import create_engine, Boolean
from sqlalchemy.orm import sessionmaker
from flask_httpauth import HTTPBasicAuth
import hashlib
from models import User, Announcement
from schemas import Announcement_Schema, User

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
def add_announcement():
    try:
        announcement = Announcement_Schema().load(request.json)
        session.add(announcement)
        session.commit()
        return 'Successful operation', 200
    except ValidationError:
        return 'Invalid input', 404


@app.route('/announcement/<uid>', methods=['GET'])
def get_announcement_by_id(uid):
    announcement = session.query(Announcement).filter_by(uid=uid).first()
    if announcement is not None:
        return Announcement_Schema().dump(announcement), 200
    return 'Announcement does not exist', 404


@app.route('/announcement/<uid>', methods=['PUT'])
def update_announcement_by_id(uid):
    try:
        query = session.query(Announcement).filter_by(uid=uid)
        query_first = query.first()
        announcement = Announcement_Schema().load(request.json)
        Announcement_Schema().dump(announcement)
        dictionary = announcement._asdict()
        dictionary['uid'] = uid
        query.update(dictionary)
        session.commit()
        return 'Successful operation', 200
    except ValidationError:
        return 'Invalid input', 404


@app.route('/announcement/<uid>', methods=['DELETE'])
def delete_announcement_by_ud(uid):
    try:
        query = session.query(Announcement).filter_by(uid=uid)
        query_first = query.first()
        if query_first is not None:
            session.delete(query_first)
            session.commit()
            return 'Successful operation', 200
        else:
            return 'Announcement does not exist', 409
    except ValidationError:
        return 'Invalid input', 404


if __name__ == 'main':
    app.run()
