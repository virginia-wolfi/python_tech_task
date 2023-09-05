from ..db import db
from ..models.task import TaskModel
from ..models.user import UserModel
from sqlalchemy.sql.selectable import Select
from flask_sqlalchemy.pagination import SelectPagination


def paginate_tasks(select: Select, page=1, per_page=5) -> SelectPagination:
    return db.paginate(select=select, page=page, per_page=per_page)
