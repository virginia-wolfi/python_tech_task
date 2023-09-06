from flask_restx import reqparse

task_parser = reqparse.RequestParser()
task_parser.add_argument(
    "page", type=int, location="args", help="which search page to display", default=1
)
task_parser.add_argument(
    "per page", type=int, location="args", help="tasks per page", default=5
)
task_parser.add_argument(
    "title",
    type=str,
    location="args",
    help="specify title search criteria",
    store_missing=False,
)
task_parser.add_argument(
    "username",
    type=str,
    location="args",
    help="specify username search criteria",
    store_missing=False,
)
task_parser.add_argument(
    "status",
    type=str,
    location="args",
    help="specify status search criteria",
    store_missing=False,
    choices=["new", "in progress", "completed", "postponed"],
)
task_parser.add_argument(
    "description",
    type=str,
    location="args",
    help="specify description search criteria",
    store_missing=False,
)
