import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from config import Config, BASE_DIR

app = Flask(__name__)
app.config.from_object(Config)
app.app_context().push()

db = SQLAlchemy()
db.init_app(app)

flask_bcrypt = Bcrypt()
flask_bcrypt.init_app(app)

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)