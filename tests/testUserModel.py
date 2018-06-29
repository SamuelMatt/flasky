# -*- coding: utf-8 -*-

import time
from unittest import TestCase
from app import create_app, db
from app.models import User


class UserModelTestCase(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='pass')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='pass')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verifycation(self):
        u = User(password='pass')
        self.assertTrue(u.verify_password('pass'))
        self.assertFalse(u.verify_password('pas'))

    def test_password_salts_are_random(self):
        u1 = User(password='pass')
        u2 = User(password='pass')
        self.assertTrue(u1.password_hash != u2.password_hash)

    def test_valid_confirmation_token(self):
        u = User(password='pass')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    def test_invalid_confirmation_token(self):
        u1 = User(password='pass1')
        u2 = User(password='pass2')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    def test_expired_confirmation_token(self):
        u = User(password='pass')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(u.confirm(token))

    def test_valid_reset_token(self):
        u = User(password='pass')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertTrue(u.reset_password(token, 'pas'))
        self.assertTrue(u.verify_password('pas'))

    def test_invalid_reset_token(self):
        u1 = User(password='pass1')
        u2 = User(password='pass2')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_reset_token()
        self.assertFalse(u2.reset_password(token, 'pass'))
        self.assertTrue(u2.verify_password('pass2'))

    def test_valid_email_change_token(self):
        u = User(email='user@email.org', password='pass')
        db.session.add(u)
        db.session.commit()
        token = u.generate_email_change_token('use@email.org')
        self.assertTrue(u.change_email(token))
        self.assertTrue(u.email == 'use@email.org')

    def test_invalid_email_change_token(self):
        u1 = User(email='user1@email.org', password='pass1')
        u2 = User(email='user2@email.org', password='pass2')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u.generate_email_change_token('user3@email.org')
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u2.email == 'user4@email.org')

    def test_duplicate_email_change_token(self):
        u1 = User(email='user1@email.org', password='pass1')
        u2 = User(email='user2@email.org', password='pass2')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u2.generate_email_change_token('user1@email.org')
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u2.email == 'user2@email.org')
