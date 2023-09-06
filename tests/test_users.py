import pytest
from to_do_list.models.user import UserModel
from testing_data import user_1
from testing_parameters import register_user_params


@pytest.mark.parametrize(("json", "message", "status_code"), register_user_params)
def test_register_validate_input(client, json, message, status_code):
    response = client.post("/registration", json=json)
    assert message in response.data
    assert status_code == response.status_code


@pytest.mark.parametrize(
    ("username", "password", "message", "status_code"),
    (
        (user_1["username"], user_1["password"], b"access_token", 200),
        ("", "123456", b"Wrong username or password", 400),
        ("Wrong username", "Wrong password", b"Wrong username or password", 400),
    ),
)
def test_login_validate_input(
    client, user, auth_action, username, password, message, status_code
):
    response = auth_action.login(username, password)
    assert message in response.data
    assert status_code == response.status_code


def test_logout_validate(client, auth_action, user):
    username, password = user
    jwt = auth_action.login(username, password).json["access_token"]
    response = auth_action.logout(jwt)
    assert b"User logged out successfully" in response.data
    assert 200 == response.status_code

    response = client.get("/profile", headers={"Authorization": f"Bearer {jwt}"})
    assert b"Log in to see this page" in response.data
    assert 401 == response.status_code


def test_profile_get(client, user, auth_action):
    username, password = user
    jwt = auth_action.login(username, password).json["access_token"]
    response = client.get("/profile", headers={"Authorization": f"Bearer {jwt}"})
    assert b"User's profile" in response.data
    assert username == response.json["User's profile"]["username"]
    assert 200 == response.status_code


def test_profile_delete(client, user, auth_action, app):
    username, password = user
    jwt = auth_action.login(username, password).json["access_token"]
    response = client.delete("/profile", headers={"Authorization": f"Bearer {jwt}"})
    assert b"Profile deleted" in response.data
    assert 200 == response.status_code
    with app.app_context():
        assert UserModel.find_by_username(username) is None
    response = client.get("/profile", headers={"Authorization": f"Bearer {jwt}"})
    assert b"Log in to see this page" in response.data
    assert 401 == response.status_code
