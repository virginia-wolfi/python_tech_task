from .db import db
from flask.cli import AppGroup


db_cli = AppGroup("db")


@db_cli.command("create")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@db_cli.command("delete")
def delete_db():
    db.drop_all()
    db.session.commit()
