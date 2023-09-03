from ..db import db


class TaskModel(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(
        db.Enum("new", "in progress", "completed", "postponed", name="status_enum")
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    @classmethod
    def find_by_id(cls, _id: int) -> "TaskModel":
        return db.session.scalars(db.select(cls).filter_by(id=_id)).first()

    @classmethod
    def find_all(cls) -> list["TaskModel"]:
        return db.session.scalars(db.select(cls)).all()
