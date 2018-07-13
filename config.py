# -*- coding: utf-8 -*-

import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_PORT = 25
    MAIL_USE_SSL = False
    MAIL_USE_TLS = False
    MAIL_SERVER = 'smtp.wo.cn'
    MAIL_USERNAME = 'ms_achencer@wo.cn'
    MAIL_PASSWORD = 'Mojiezuo_1991'
    FLASK_MAIL_SUBJECT_PREFIX = '[Flask]'
    FLASK_ADMIN = 'ms_achencer@wo.cn'
    FLASK_MAIL_SENDER = 'Flask Admin <ms_achencer@wo.cn>'
    FLASK_FOLLOWERS_PER_PAGE = 50
    FLASK_POSTS_PER_PAGE = 20
    FLASK_COMMENTS_PER_PAGE = 30

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+pymysql://matt:mojiezuo1991@localhost/flaskdev'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'mysql+pymysql://matt:mojiezuo1991@localhost/flasktest'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://matt:mojiezuo1991@localhost/flaskprodu'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig}
