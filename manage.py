#!/usr/bin/env python

import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from app.models import User, Role

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_contex():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command('shell', Shell(make_context=make_shell_contex))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    from unittest import TestLoader, TextTestRunner
    tests = TestLoader().discover('tests')
    TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
    # app.run()
