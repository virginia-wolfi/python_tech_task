from to_do_list.db import db


def save_to_db(model: db.Model) -> None:
    db.session.add(model)
    db.session.commit()


def delete_from_db(model: db.Model) -> None:
    db.session.delete(model)
    db.session.commit()
