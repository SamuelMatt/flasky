from os import path, environ

basedir = path.abspath(path.dirname(__file__))
SECRET_KEY = 'hard to guess string'
SQLALCHEMY_DATABASE_URI = f"sqlite:///{path.join(basedir, 'data.sqlite')}"
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
MAIL_SERVER = '127.0.0.1'
MAIL_PORT = 25
MAIL_USE_SSL = False
MAIL_USE_TLS = False
MAIL_USERNAME = environ.get('MAIL_USERNAME')
MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
FLASK_MAIL_SUBJECT_PREFIX = '[Flask]'
FLASK_ADMIN = environ.get('FLASK_ADMIN')
FLASK_MAIL_SENDER = f'Flask Admin <{FLASK_ADMIN}>'
