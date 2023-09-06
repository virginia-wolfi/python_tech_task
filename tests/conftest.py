import pytest
import os
import dotenv

dotenv.load_dotenv(os.getenv(".env"))
from to_do_list import create_app
from to_do_list.db import db
from to_do_list.config import TestingConfig
from to_do_list.models.user import UserModel
from to_do_list.models.task import TaskModel
from testing_data import user_1, user_2, task_1, tasks
from to_do_list.operations import save_to_db, delete_from_db
from testing_classes import AuthActions, TaskActions


@pytest.fixture(scope="session")
def app():
    app = create_app(TestingConfig())
    with app.app_context():
        db.drop_all()
        db.create_all()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def user(app):
    with app.app_context():
        user = UserModel(**user_1)
        save_to_db(user)
        username = user.username
        password = user.password
    yield username, password
    with app.app_context():
        if UserModel.find_by_username(username):
            delete_from_db(user)


@pytest.fixture(scope="session")
def another_user(app):
    with app.app_context():
        user = UserModel(**user_2)
        save_to_db(user)
        username = user.username
        password = user.password
    yield username, password
    with app.app_context():
        if UserModel.find_by_username(username):
            delete_from_db(user)


@pytest.fixture()
def task_id(user, app):
    username, password = user
    with app.app_context():
        db.session.execute(db.text("TRUNCATE TABLE tasks"))
        user_id = UserModel.find_by_username(username).id
        new_task = TaskModel(**task_1, user_id=user_id)
        save_to_db(new_task)
        yield new_task.id


@pytest.fixture
def user_jwt(user, auth_action):
    username, password = user
    jwt = auth_action.login(username, password).json["access_token"]
    return jwt


@pytest.fixture
def another_user_jwt(another_user, auth_action):
    username, password = another_user
    jwt = auth_action.login(username, password).json["access_token"]
    return jwt


@pytest.fixture
def created_tasks(app, user):
    with app.app_context():
        db.session.execute(db.text("TRUNCATE TABLE tasks"))
        username = user[0]
        user_id = UserModel.find_by_username(username).id
        for task in tasks:
            save_to_db(TaskModel(user_id=user_id, **task))
        number_added = len(tasks)
    yield number_added


@pytest.fixture
def auth_action(client):
    return AuthActions(client)


@pytest.fixture
def task_action(client):
    return TaskActions(client)
