import os

from flask import Flask, make_response
from .config import DevelopmentConfig
from .db import db
from .models.user import UserModel
from .models.task import TaskModel
from .models.blocked_token import TokenBlocklist
from .cli import db_cli
from .resources import api
from .jwt import jwt
from datetime import timedelta


def create_app(config_obj=DevelopmentConfig()):
    app = Flask(__name__)
    app.config.from_object(config_obj)
    if os.getenv("DATABASE_URL"):
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    ACCESS_EXPIRES = timedelta(hours=1)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
    app.json.sort_keys = False
    app.json.ensure_ascii = False
    db.init_app(app)
    app.cli.add_command(db_cli)
    jwt.init_app(app)
    api.init_app(app)

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return UserModel.query.filter_by(id=identity).one_or_none()

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

        return token is not None

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return make_response(
            {
                "description": "Log in to see this page",
            },
            401,
        )

    return app
