create_task_params = (
    (
        {"title": "Test_title", "description": "Test_description", "status": "new"},
        b"Created new task",
        201,
    ),
    (
        {"description": "Test_description", "status": "new"},
        b"Input payload validation failed",
        400,
    ),
    (
        {
            "title": "Test_title",
            "description": "Test_description",
            "status": "not correct status",
        },
        b"'not correct status' is not one of ['new', 'in progress', 'completed', 'postponed']",
        400,
    ),
)

update_task_params = (
    ({"status": "new"}, b"Updated task", 200),
    ({"title": "New title", "status": "new"}, b"Updated task", 200),
    ({"description": "New_decription"}, b"Updated task", 200),
    ({}, b"Incorrect or absent fields", 400),
    ({"title": ""}, b'"title": "\'\' is too short"', 400),
    ({"status": "incorrect_status"}, b"Input payload validation failed", 400),
)

select_task_params = (
    ({"username": "test_name_1"}, b"title", 200),
    (
        {"username": "unknown_username"},
        b"The requested URL was not found on the server",
        404,
    ),
    ({"title": "User_1_task_1"}, b"title", 200),
    ({"title": "Unknown_title"}, b"The requested URL was not found on the server", 404),
    ({"page": 5}, b"The requested URL was not found on the server", 404),
    ({"description": "Test_description_1"}, b"title", 200),
    ({"status": "new", "title": "User_1_task_1"}, b"title", 200),
)

register_user_params = (
    (
        {
            "first_name": "User_first_name",
            "last_name": "User_last_name",
            "username": "username_1",
            "password": "123456",
        },
        b"User created",
        201,
    ),
    (
        {
            "first_name": "User_first_name",
            "last_name": "User_last_name",
            "username": "username_1",
            "password": "123456",
        },
        b"This username is taken",
        400,
    ),
    (
        {
            "first_name": "",
            "last_name": "User_last_name",
            "username": "username_2",
            "password": "123456",
        },
        b"Input payload validation failed",
        400,
    ),
    (
        {
            "first_name": "User_first_name",
            "last_name": "User_last_name",
            "username": "",
            "password": "123456",
        },
        b"Input payload validation failed",
        400,
    ),
)
