from .models.task import TaskModel
from .db import db
from sqlalchemy import and_


def find_all(model: db.Model) -> list[db.Model]:
    return db.session.scalars(db.select(model)).all()


def save_to_db(model: db.Model) -> None:
    db.session.add(model)
    db.session.commit()


def delete_from_db(model: db.Model) -> None:
    db.session.delete(model)
    db.session.commit()


def find_tasks(**kwargs) -> list[TaskModel]:
    filters = []
    non_str_attrs = (
        ("id", TaskModel.id),
        ("user_id", TaskModel.user_id),
        ("status", TaskModel.status),
    )
    str_attrs = (("title", TaskModel.title), ("description", TaskModel.description))

    for name, model_attr in non_str_attrs:
        if name in kwargs:
            filters.append(model_attr == kwargs[name])

    for name, model_attr in str_attrs:
        if name in kwargs:
            filters.append(model_attr.icontains(kwargs[name]))
    return db.session.scalars(db.select(TaskModel).where(and_(*filters))).all()


def update_task(id, **kwargs) -> None:
    db.session.query(TaskModel).filter_by(id=id).update(kwargs)
    db.session.commit()
