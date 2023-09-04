from flask_restx import Api
from .user import users, UserRegister, UserLogin, UserLogout, UserProfile
from .api_models.task import task_creation_fields
from .api_models.user import registration_fields, login_fields, user_brief_fields
from .tasks import tasks, Task, TaskDelete

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

api.add_namespace(users)