from flask_restx import Resource, Namespace, marshal
from flask_jwt_extended import jwt_required, current_user

from flask import request, jsonify, abort, make_response
from ..operations import save_to_db, delete_from_db
from ..operations.task import update_task, find_tasks
from ..operations.pagination import paginate_tasks
from ..models.task import TaskModel
from ..models.user import UserModel
from .api_models.task import (
    repr_task_fields,
    creation_task_fields,
    brief_task_fields,
    update_task_fields,
)
from .api_models.parsers import task_parser

tasks = Namespace("Tasks", description="Tasks related operations", path="/tasks")


class TaskSelect(Resource):
    @jwt_required()
    @tasks.expect(task_parser)
    @tasks.doc(security="Bearer Auth")
    def get(self):
        """Gets tasks with provided criteria"""
        tasks = dict()
        args = task_parser.parse_args()
        page = args.pop("page")
        per_page = args.pop("per page")
        if not args:
            all_tasks = TaskModel.select_all()
        else:
            if args.get("username", None):
                try:
                    args["user_id"] = UserModel.find_by_username(args["username"]).id
                except AttributeError:
                    abort(400, "Username was not found")
                args.pop("username")
            all_tasks = find_tasks(**args)
        paginated = paginate_tasks(all_tasks, page, per_page)
        for task in paginated:
            tasks[f"Task id {task.id}"] = marshal(task, repr_task_fields)
        return make_response(jsonify(tasks), 200)


class TaskCreate(Resource):
    @jwt_required()
    @tasks.expect(creation_task_fields)
    @tasks.doc(security="Bearer Auth")
    @tasks.marshal_with(brief_task_fields, envelope="Created new task")
    def post(self):
        """Creates a new task"""
        id = current_user.id
        input_data = marshal(request.get_json(), creation_task_fields)
        new_task = TaskModel(user_id=id, **input_data)
        save_to_db(new_task)
        return new_task, 201


class Task(Resource):
    @jwt_required()
    @tasks.doc(security="Bearer Auth")
    @tasks.marshal_with(repr_task_fields)
    def get(self, task_id):
        """Gets task with provided id"""
        task = TaskModel.find_by_id(task_id)
        if not task:
            abort(404, "Task was not found")
        return task, 200

    @jwt_required()
    @tasks.expect(update_task_fields)
    @tasks.doc(security="Bearer Auth")
    @tasks.marshal_with(brief_task_fields, envelope="Updated task")
    def patch(self, task_id):
        """Updates a task with provided id.
        Fields available for update: title, description, status"""
        user = current_user
        task = TaskModel.find_by_id(task_id)
        if not task:
            abort(404, "Task was not found")
        if task not in user.tasks:
            abort(403, "Only owner can make changes in task")
        input_data = marshal(request.get_json(), creation_task_fields, skip_none=True)
        if not input_data:
            abort(400, "Incorrect or absent fields")
        update_task(task_id, **input_data)
        return task, 200

    @jwt_required()
    @tasks.doc(security="Bearer Auth")
    def delete(self, task_id):
        """Deletes a task with provided id"""
        user = current_user
        task = TaskModel.find_by_id(task_id)
        if not task:
            abort(404, "Task was not found")
        if task not in user.tasks:
            abort(403, "Only owner can delete task")
        delete_from_db(task)
        return make_response(jsonify({"message": f"Deleted task {task_id}"}), 200)
