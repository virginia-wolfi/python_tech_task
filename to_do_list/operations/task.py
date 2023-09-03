from ..models.task import TaskModel
from ..db import db
from sqlalchemy import and_


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


def update_task(id: int, **kwargs) -> None:
    db.session.query(TaskModel).filter_by(id=id).update(kwargs)
    db.session.commit()
