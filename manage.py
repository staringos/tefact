from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from arrplat.app import app, db
from arrplat.setup import application_data

Migrate(app=app, db=db, render_as_batch=True, compare_type=True, compare_server_default=True)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('init-data', application_data)

if __name__ == '__main__':
    manager.run()
