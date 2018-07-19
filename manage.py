#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand, upgrade
from app import db, create_app
from app.models import Permission, Role, Follow, User, Post, \
    Comment

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_contex():
    return dict(app=app, db=db, Permission=Permission, Role=Role,
                Follow=Follow, User=User, Post=Post, Comment=Comment)


manager.add_command('shell', Shell(make_context=make_shell_contex))
manager.add_command('db', MigrateCommand)


if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]


@manager.command
def profile(length=25, profile_dir=None):
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(
        app.wsgi_app, restrictions=[length], profile_dir=profile_dir)
    app.run()


@manager.command
def deploy():
    upgrade()
    Role.insert_roles()
    User.add_self_follows()


COV = None
if os.environ.get('FLASK_COVERAGE'):
    from coverage import coverage
    COV = coverage(branch=True, include='app/*')
    COV.start()


@manager.command
def test(coverage=False):
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print(f'HTML version: file://{covdir}/index.html')
        COV.erase()


if __name__ == '__main__':
    manager.run()
