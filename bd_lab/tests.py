import base64
from flask import Flask, jsonify
from flask_testing import TestCase
import unittest
from app import app, session, metadata, engine
from sqlalchemy.orm import close_all_sessions
import hashlib
from pprint import pprint


from models import User, Announcement, Category, Base


class TestingViews(TestCase):

    @classmethod
    def setUpClass(cls):
        Base.metadata.drop_all(bind=engine)
        # metadata.reflect(bind=engine)
        # pass

    # creates instance of flask app
    def create_app(self):
        return app

    def setUp(self):
        session.commit()
        Base.metadata.create_all(engine)
        session.commit()
        user1 = User(name='nestor', location='lviv', username='nstr', password='d8578edf8458ce06fbc5bb76a58c5ca4')
        user2 = User(name='anon', location='kyiv', username='anon', password='d8578edf8458ce06fbc5bb76a58c5ca4')
        session.add_all([user1, user2])
        session.flush()

        local_post_lviv = Announcement(name="local_post_lviv", releaseDate="today",local=True, location="lviv")
        local_post_kyiv = Announcement(name="local_post_kyiv", releaseDate="today",local=True, location="kyiv")
        public_post_lviv = Announcement(name="public_post_lviv", releaseDate="today",local=False, location="lviv")
        local_post_lviv.owner_uid=user1.uid
        local_post_kyiv.owner_uid=user2.uid
        public_post_lviv.owner_uid=user1.uid
        session.add_all([local_post_lviv, public_post_lviv, local_post_kyiv])
        session.commit()

    def tearDown(self):
        close_all_sessions()
        Base.metadata.drop_all(bind=engine)

    def open_with_auth(self, url, method, username, password, **kwargs):
        return self.client.open(url,
                                method=method,
                                headers={
                                    'Authorization': 'Basic ' +
                                    base64.b64encode(
                                        bytes(username + ":" + password, 'ascii')).decode('ascii')
                                },
                                **kwargs
                                )
    # 34
    def test_user_in_session(self):
        self.assertIn(session.query(User).filter_by(username='nstr').first(), session)

    # 42
    def test_register(self):
        data = {

            "name": "test_name",
            "location": "test_location",
            "username": "test_username",
            "password": "test_password"
        }
        res = self.client.open('/register', method='POST', json=data)
        self.assert200(res)
        self.assertIsNotNone(session.query(User).filter_by(username='test_username').scalar())

        res = self.client.open('/register', method='POST', json=data)
        self.assertEqual(res.data, b'Username is already in use')
    # 50%
    def test_get_user_by_username(self):
        # getting my own username without auth
        res = self.client.open('/user/nstr', method='GET')
        self.assertEqual(res.data, b'Unauthorized Access')
        # getting my own username with auth
        res = self.open_with_auth('/user/nstr', 'GET', 'nstr', 'qwerty')
        self.assert200(res)
        # getting others username
        res = self.open_with_auth('/user/anon', 'GET', 'nstr', 'qwerty')
        self.assertEqual(res.data, b'Access denied')

    def test_delete_user(self):
        user = session.query(User).filter_by(username='nstr').scalar()
        self.assertIsNotNone(user)
        res = self.open_with_auth('/user', 'DELETE', 'nstr', 'qwerty')
        deletedUser = session.query(User).filter_by(username='nstr').scalar()
        self.assertIsNone(deletedUser)
        # - deletion of dependencies
        self.assertIsNone(session.query(Announcement).filter_by(owner_uid=user.uid).scalar())
        self.assertEqual(res.data, b'Successful operation')
    # 63%
    def test_update_user(self):
        # change myself:
        user = session.query(User).filter_by(username='nstr').scalar()

        data = {
            "name": "changed_name",
            "location": "changed_location",
        }
        res = self.open_with_auth('/user', 'PUT', 'nstr', 'qwerty', json=data)
        pprint(res.data)
        changeduser = session.query(User).filter_by(username='nstr').scalar()
        self.assertEqual(changeduser.name, 'changed_name')
        res = self.open_with_auth('/user', 'PUT', 'nstr', 'qwerty', json={})
        self.assertStatus(res, 404)
    # 72 
    def test_add_announcement(self):
        user = session.query(User).filter_by(username='nstr').scalar()

        data = {
            "name": "test_announcement_name",
            "releaseDate": "test_announcement_releaseDate",
            "local": True,
            "location": "test_announcement_location"
        }
        res = self.open_with_auth('/add_announcement', 'POST', 'nstr', 'qwerty', json=data)
        self.assert200(res)
        new_post = session.query(Announcement).filter_by(name="test_announcement_name").scalar()
        self.assertIsNotNone(new_post)
        self.assertEqual(new_post.owner_uid, user.uid)
        
        res = self.open_with_auth('/add_announcement', 'POST', 'nstr', 'qwerty', json={"bad":"data"})
        self.assert404(res)

    # 75
    def test_get_announcement_by_id(self):
        user = session.query(User).filter_by(username='nstr').scalar()
        local_post_lviv_id = session.query(Announcement).filter_by(name='local_post_lviv').scalar().uid
        local_post_kyiv_id = session.query(Announcement).filter_by(name='local_post_kyiv').scalar().uid
        public_post_lviv_id = session.query(Announcement).filter_by(name='public_post_lviv').scalar().uid
        
        res = self.open_with_auth(f'/announcement/{local_post_lviv_id}', 'GET', 'nstr', 'qwerty')
        self.assert200(res)

        res = self.open_with_auth(f'/announcement/{local_post_kyiv_id}', 'GET', 'nstr', 'qwerty')
        self.assert403(res)
        
        res = self.open_with_auth(f'/announcement/{local_post_kyiv_id}', 'GET', 'anon', 'qwerty')
        self.assert200(res)
        
        res = self.open_with_auth(f'/announcement/{public_post_lviv_id}', 'GET', 'anon', 'qwerty')
        self.assert200(res)
        
        res = self.open_with_auth(f'/announcement/2934832', 'GET', 'nstr', 'qwerty')
        self.assert404(res)

    # 87
    def test_update_announcement_by_id(self):
        user = session.query(User).filter_by(username='nstr').scalar()
        local_post_lviv_id = session.query(Announcement).filter_by(name='local_post_lviv').scalar().uid
        data = {
            "name":"local_post_lviv_id_changed"
        }
        res = self.open_with_auth(f'/announcement/{local_post_lviv_id}', 'PUT', 'nstr', 'qwerty', json=data)
        self.assert200(res)

        res = self.open_with_auth(f'/announcement/{local_post_lviv_id}', 'PUT', 'anon', 'qwerty', json=data)
        # pprint(res.data)
        self.assertStatus(res, 409)
        
        res = self.open_with_auth(f'/announcement/39048293', 'PUT', 'anon', 'qwerty', json=data)
        self.assert404(res)
        
        res = self.open_with_auth(f'/announcement/39048293', 'PUT', 'anon', 'qwerty', json={"bad":"data"})
        self.assert404(res)

        self.assertEqual(session.query(Announcement).get(local_post_lviv_id).name, "local_post_lviv_id_changed")

    def test_delete_announcement_by_id(self):
        user = session.query(User).filter_by(username='nstr').scalar()
        local_post_lviv_id = session.query(Announcement).filter_by(name='local_post_lviv').scalar().uid

        res = self.open_with_auth(f'/delete_announcement/{local_post_lviv_id}', 'DELETE', 'anon', 'qwerty')
        self.assertStatus(res, 409)

        res = self.open_with_auth(f'/delete_announcement/{local_post_lviv_id}', 'DELETE', 'nstr', 'qwerty')
        pprint(res.data)
        self.assert200(res)

        res = self.open_with_auth(f'/delete_announcement/29384230', 'DELETE', 'nstr', 'qwerty')
        self.assert404(res)

    

if __name__ == '__main__':
    unittest.main()
