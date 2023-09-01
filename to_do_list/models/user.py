from ..db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.Text, nullable=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(
        db.String, db.CheckConstraint("char_length(password) > 5"), nullable=False
    )
    tasks = db.relationship("TaskModel", backref="user")


