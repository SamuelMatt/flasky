from flask_script import Manager, Shell
from flask_migrate import MigrateCommand
from app import app
from app.models import makeShellContex

manager = Manager(app)

manager.add_command('shell', Shell(make_context=makeShellContex))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run(
        # debug=False
    )
