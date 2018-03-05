from os import path, environ
from threading import Thread
from flask import Flask, render_template, session, redirect, url_for
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message

basedir = path.abspath(path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{path.join(basedir, 'data.sqlite')}"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = '127.0.0.1'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = environ.get('MAIL_PASSWORD')
app.config['FLASK_MAIL_SUBJECT_PREFIX'] = '[Flask]'
app.config['FLASK_ADMIN'] = environ.get('FLASK_ADMIN')
app.config['FLASK_MAIL_SENDER'] = f"Flask Admin <{app.config['FLASK_ADMIN']}>"

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)


class NameForm(FlaskForm):
    name = StringField("What's your name?", validators=[Required()])
    submit = SubmitField('Submit')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return f'<Role {self.name!r}>'


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    roleId = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return f'<User {self.username!r}>'


def makeShellContex():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command('shell', Shell(make_context=makeShellContex))
manager.add_command('db', MigrateCommand)


def sendAsyncMail(app, msg):
    with app.app_context():
        mail.send(msg)


def sendMail(to, subject, template, **kwargs):
    msg = Message(
        subject=app.config['FLASK_MAIL_SUBJECT_PREFIX'] + subject,
        sender=app.config['FLASK_MAIL_SENDER'],
        recipients=[to]
    )
    msg.body = render_template(f'{template}.txt', **kwargs)
    msg.html = render_template(f'{template}.html', **kwargs)
    thr = Thread(target=sendAsyncMail, args=[app, msg])
    thr.start()
    return thr


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['know'] = False
            if app.config['FLASK_ADMIN']:
                sendMail(
                    app.config['FLASK_ADMIN'],
                    'New User',
                    'mail/new_user',
                    user=user
                )
        else:
            session['know'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template(
        'index.html',
        form=form,
        name=session.get('name'),
        know=session.get('know', False)
    )


@app.route('/user/<name>')
def user(name):
    return render_template(
        'user.html',
        name=name
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    manager.run(
        debug=False
    )

    # app.run(
    #     debug=False
    # )
