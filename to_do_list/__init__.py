import os

from flask import Flask
from .config import DevelopmentConfig
from .db import db
from .models.user import UserModel
from .models.task import TaskModel
from .cli import db_cli


def create_app(config_obj=DevelopmentConfig()):
    app = Flask(__name__)
    app.config.from_object(config_obj)
    if os.getenv("DATABASE_URL"):
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.json.sort_keys = False
    app.json.ensure_ascii = False
    db.init_app(app)
    app.cli.add_command(db_cli)

    return app
