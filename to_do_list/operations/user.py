from ..models.user import UserModel
from ..db import db


def update_user(id: int, **kwargs) -> None:
    db.session.query(UserModel).filter_by(id=id).update(kwargs)
    db.session.commit()
