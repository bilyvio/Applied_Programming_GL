from flask import Flask, request, jsonify
from marshmallow import ValidationError
from sqlalchemy import create_engine, Boolean, MetaData
from sqlalchemy.orm import sessionmaker
from flask_httpauth import HTTPBasicAuth
import hashlib
from models import User, Announcement, Category, Base
from schemas import Announcement_Schema, User_Schema

engine = create_engine("postgresql://violetta:12345@localhost:5432/my_database")
Session = sessionmaker(bind=engine)
session = Session()

auth = HTTPBasicAuth()
app = Flask(__name__)
app.debug = True
app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = False

metadata = MetaData()

Base.metadata.create_all(engine)
# Category.create(engine, checkfirst=False)
# Announcement.create(engine, checkfirst=False)
# User.create(engine, checkfirst=False)
# metadata.drop_all(bind=engine)
# metadata.create_all(bind=engine)
# session.commit()

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
    user = session.query(User).filter_by(username=username,
                                                password=hashlib.md5(password.encode()).hexdigest()).first()
    if user:
        return user


@app.route('/user/<username>', methods=['GET'])
@auth.login_required
def get_user_by_username(username):
    user = session.query(User).filter_by(username=username).first()
    if auth.current_user().uid != user.uid:
        return 'Access denied', 403
    else:
        return jsonify(user._asdict()), 200



@app.route('/user', methods=['PUT'])
@auth.login_required
def update_user():
    current = auth.current_user()
    data = request.get_json()
    if data.get('name') or data.get('location'):
        name = data.get('name', current.name)
        location = data.get('location', current.location)
        user = auth.current_user()
        user.name = name
        user.location = location
        session.commit()
        return 'Successful operation', 200
    else:
        return 'Invalid input', 404


@app.route('/user', methods=['DELETE'])
@auth.login_required
def delete_user():
    # try:
    session.query(Announcement).filter_by(owner_uid=auth.current_user().uid).delete()
    session.delete(auth.current_user())
    session.commit()
    return 'Successful operation', 200
    # except ValidationError:
        # return 'Invalid input', 404


@app.route('/add_announcement', methods=['POST'])
@auth.login_required
def add_announcement():
    try:
        # user = session.query(User).filter_by(username=auth.current_user()).first()
        user = auth.current_user()
        print(user)
        announcement = Announcement_Schema().load(request.json)
        announcement.owner_uid = user.uid
        session.add(announcement)
        session.commit()
        return 'Successful operation', 200
    except ValidationError as error:
        print(error)
        return 'Invalid input', 404


@app.route('/announcement/<uid>', methods=['GET'])
@auth.login_required(optional=True)
def get_announcement_by_id(uid):
    announcement = session.query(Announcement).filter_by(uid=int(uid)).first()
    if announcement is not None:
        if auth.current_user() is None:
            if not announcement.local:
                return Announcement_Schema().dump(announcement), 200
        elif not announcement.local or announcement.location == auth.current_user().location:
            return Announcement_Schema().dump(announcement), 200

        return 'This local announcement is not available to you', 403
    return 'Announcement does not exist', 404


@app.route('/announcement/<uid>', methods=['PUT'])
@auth.login_required
def update_announcement_by_id(uid):
    try:
        user = auth.current_user()
        announcement = Announcement_Schema().load(request.json)
        announcement_up = session.query(Announcement).get(uid)
        if announcement_up is None:
            return 'Announcement does not exist', 404
        if user.uid != announcement_up.owner_uid:
            return 'Announcement does not belong to user', 409
        announcement_up.name = announcement.name
        announcement_up.releaseDate = announcement.releaseDate
        announcement_up.location = announcement.location
        announcement_up.local = announcement.local
        session.commit()
        return 'Successful operation', 200
    except ValidationError:
        return 'Invalid input', 404


@app.route('/delete_announcement/<uid>', methods=['DELETE'])
@auth.login_required
def delete_announcement_by_id(uid):
    user = auth.current_user()
    announcement_up = session.query(Announcement).get(uid)
    if announcement_up is None:
        return 'Announcement does not exist', 404
    if user.uid != announcement_up.owner_uid:
        return 'Announcement does not belong to user', 409
    session.delete(announcement_up)
    session.commit()
    return 'Successful operation', 200



if __name__ == '__main__':
    app.run(debug=True)
