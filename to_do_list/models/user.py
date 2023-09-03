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

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return db.session.scalars(db.select(cls).filter_by(username=username)).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return db.session.scalars(db.select(cls).filter_by(id=_id)).first()
