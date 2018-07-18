# -*- coding: utf-8 -*-

import re
from time import sleep
from threading import Thread
from unittest import TestCase
from selenium import webdriver
from app import create_app, db
from app.models import Role, User, Post


class SeleniumTestCase(TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        try:
            cls.client = webdriver.Chrome()
        except:
            pass

        if cls.client:
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            from logging import getLogger
            logger = getLogger('werkzeug')
            logger.setLevel("ERROR")

            db.create_all()
            Role.insert_roles()
            User.generate_fake(10)
            Post.generate_fake(10)

            admin_role = Role.query.filter_by(permissions=0b11111111).first()
            admin = User(email='john@example.com', username='john',
                         password='cat', role=admin_role, confirmed=True)
            db.session.add(admin)
            db.session.commit()

            Thread(target=cls.app.run).start()
            sleep(1)

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            cls.client.get('http://127.0.0.1/shutdown')
            cls.client.close()

            db.drop_all()
            db.session.remove()

            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass

    def test_admin_home_page(self):
        self.client.get('http://127.0.0.1/')
        self.assertTrue(re.search(
            r'Hello,\s+Chencer!', self.client.page_source))

        self.client.find_element_by_link_text('Log In').click()
        self.assertTrue('<h1>Login</h1>' in self.client.page_source)

        self.client.find_element_by_name('email').send_keys('john@example.com')
        self.client.find_element_by_name('password').send_keys('cat')
        self.client.find_element_by_name('submit').click()
        self.assertTrue(re.search(r'Hello,\s+john!', self.client.page_source))

        self.client.find_element_by_link_text('Profile').click()
        self.assertTrue('<h1>john</h1>' in self.client.page_source)
