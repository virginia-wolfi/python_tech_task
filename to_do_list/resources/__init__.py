from flask_restx import Api
from .user import users, UserRegister, UserLogin, UserLogout, UserProfile
from .api_models.task import (
    repr_task_fields,
    creation_task_fields,
    brief_task_fields,
    update_task_fields,
)
from .api_models.user import registration_fields, login_fields, user_brief_fields
from .tasks import tasks, TaskSelect, Task, TaskCreate

authorizations = {
    "Bearer Auth": {"type": "apiKey", "in": "header", "name": "Authorization"},
}
api = Api(
    title="ToDo app",
    version="1.0",
    description="A simple RESTful API application for managing a task list",
    validate=True,
    authorizations=authorizations,
    security="apikey",
)


users.add_model("Registration model", registration_fields)
users.add_model("Login model", login_fields)
users.add_model("User brief model", user_brief_fields)

users.add_resource(UserRegister, "/registration")
users.add_resource(UserLogin, "/login")
users.add_resource(UserLogout, "/logout")
users.add_resource(UserProfile, "/profile")

tasks.add_model("Representation task model", repr_task_fields)
tasks.add_model("Creation task model", creation_task_fields)
tasks.add_model("Task brief model", brief_task_fields)
tasks.add_model("Update task model", update_task_fields)
tasks.add_resource(TaskSelect, "")
tasks.add_resource(Task, "/<int:task_id>")
tasks.add_resource(TaskCreate, "/create")
api.add_namespace(tasks)

api.add_namespace(users)
