# manage.py

from flask.ext.script import Manager, Shell

from bookfinder import app
from bookfinder.db import connect

manager = Manager(app)


# Shell command
def _make_context():
    return dict(app=app, connect=connect)
manager.add_command("shell", Shell(make_context=_make_context))


@manager.command
def init_db():
    return connect.init_db()


@manager.command
def flush_db():
    return connect.flush_db()

if __name__ == "__main__":
    manager.run()
