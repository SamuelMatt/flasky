from os import path, environ

appdir = path.abspath(path.dirname(__file__))
basedir = path.join(appdir, 'data')


class Config:
    SECRET_KEY = environ.get('SECRET_KEY') or 'hard to guess string'
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

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URL') or \
        f"sqlite:///{path.join(basedir, 'dataDev.sqlite')}"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get('TEST_DATABASE_URL') or \
        f"sqlite:///{path.join(basedir, 'dataTest.sqlite')}"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL') or \
        f"sqlite:///{path.join(basedir, 'data.sqlite')}"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
