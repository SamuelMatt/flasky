import time
from unittest import TestCase
from app import create_app, db
from app.models import User, Role, Permission, AnonymousUser


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
        u = User(password='mas')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='mas')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verifycation(self):
        u = User(password='mas')
        self.assertTrue(u.verify_password('mas'))
        self.assertFalse(u.verify_password('mat'))

    def test_password_salts_are_random(self):
        u = User(password='mas')
        u0 = User(password='mas')
        self.assertTrue(u.password_hash != u0.password_hash)

    def test_valid_confirmation_token(self):
        u = User(password='mas')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    def test_invalid_confirmation_token(self):
        u = User(password='mas')
        u2 = User(password='msa')
        db.session.add(u)
        db.session.add(u2)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    def test_expired_confirmation_token(self):
        u = User(password='mas')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(u.confirm(token))

    def test_valid_reset_token(self):
        u = User(password='mas')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertTrue(u.reset_password(token, 'msa'))
        self.assertTrue(u.verify_password('msa'))

    def test_invalid_reset_token(self):
        u = User(password='mas')
        u2 = User(password='msa')
        db.session.add(u)
        db.session.add(u2)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertFalse(u2.reset_password(token, 'matt'))
        self.assertTrue(u2.verify_password('msa'))

    def test_valid_email_change_token(self):
        u = User(email='mas@chencer.org', password='mas')
        db.session.add(u)
        db.session.commit()
        token = u.generate_email_change_token('msa@chencer.org')
        self.assertTrue(u.change_email(token))
        self.assertTrue(u.email == 'msa@chencer.org')

    def test_invalid_email_change_token(self):
        u = User(email='mas@chencer.org', password='mas')
        u2 = User(email='msa@chencer.org', password='msa')
        db.session.add(u)
        db.session.add(u2)
        db.session.commit()
        token = u.generate_email_change_token('matt@chencer.org')
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u2.email == 'msa@chencer.org')

    def test_duplicate_email_change_token(self):
        u = User(email='mas@chencer.org', password='mas')
        u2 = User(email='msa@chencer.org', password='msa')
        db.session.add(u)
        db.session.add(u2)
        db.session.commit()
        token = u2.generate_email_change_token('mas@chencer.org')
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u2.email == 'msa@chencer.org')

    def test_roles_and_permissions(self):
        Role.insert_roles()
        u = User(email='mas@chencer.org', password='mas')
        self.assertTrue(u.can(Permission.Write_Articles))
        self.assertFalse(u.can(Permission.Moderate_Comments))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.Follow))
