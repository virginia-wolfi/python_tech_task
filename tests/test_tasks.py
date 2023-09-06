import pytest
from to_do_list.models.task import TaskModel
from testing_parameters import (
    create_task_params,
    update_task_params,
    select_task_params,
)


@pytest.mark.parametrize(("json", "message", "status_code"), create_task_params)
def test_create_task(user_jwt, task_action, json, message, status_code):
    response = task_action.create(user_jwt, **json)
    assert message in response.data
    assert status_code == response.status_code


def test_get_by_id_task(user_jwt, task_id, task_action):
    response = task_action.get_by_id(user_jwt, task_id)
    assert response.json["id"] == task_id
    assert 200 == response.status_code

    response = task_action.get_by_id(user_jwt, task_id + 1)
    assert b"Task was not found" in response.data
    assert 404 == response.status_code


def test_delete_by_id_task(user_jwt, another_user_jwt, task_id, task_action):
    response = task_action.delete_by_id(another_user_jwt, task_id)
    assert b"Only owner can delete task" in response.data
    assert 403 == response.status_code

    response = task_action.delete_by_id(user_jwt, task_id)
    assert f"Deleted task {task_id}" in response.text
    assert 200 == response.status_code

    response = task_action.get_by_id(user_jwt, task_id)
    assert b"Task was not found" in response.data
    assert 404 == response.status_code

    task = TaskModel.find_by_id(task_id)
    assert task is None


@pytest.mark.parametrize(("json", "message", "status_code"), update_task_params)
def test_update_by_id_task(user_jwt, task_id, task_action, json, message, status_code):
    response = task_action.update_by_id(user_jwt, task_id, **json)
    assert message in response.data
    assert status_code == response.status_code


def test_update_by_wrong_id_task(user_jwt, another_user_jwt, task_id, task_action):
    response = task_action.update_by_id(another_user_jwt, task_id, status="new")
    assert b"Only owner can make changes in task" in response.data
    assert 403 == response.status_code

    response = task_action.update_by_id(user_jwt, task_id + 1, status="new")
    assert b"Task was not found" in response.data
    assert 404 == response.status_code


@pytest.mark.parametrize(
    ("query_string", "status_code"),
    (
        ({}, 200),
        ({"per page": 2}, 200),
    ),
)
def test_select_tasks(user_jwt, created_tasks, task_action, query_string, status_code):
    response = task_action.select(user_jwt, **query_string)
    assert len(response.json) == query_string.get("per page", 5)
    assert status_code == response.status_code


@pytest.mark.parametrize(("query_string", "message", "status_code"), select_task_params)
def test_select_tasks_by_user(
    user_jwt, created_tasks, task_action, query_string, message, status_code
):
    response = task_action.select(user_jwt, **query_string)
    assert message in response.data
    assert status_code == response.status_code
