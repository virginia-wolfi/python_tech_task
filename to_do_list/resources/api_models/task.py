from flask_restx import fields, Model

repr_task_fields = Model(
    "Representation task model",
    {
        "id": fields.Integer(),
        "title": fields.String,
        "description": fields.String(),
        "status": fields.String(
            enum=["new", "in progress", "completed", "postponed"],
        ),
        "owner": fields.String(attribute=lambda x: x.user.username),
    },
)


creation_task_fields = Model(
    "Creation task model",
    {
        "title": fields.String(
            required=True,
            description="Task title",
            example="Finish a novel",
            min_length=4,
        ),
        "description": fields.String(
            description="Task description",
            example="Writing last chapter in the 'Son' novel",
            min_length=4,
        ),
        "status": fields.String(
            required=True,
            description="Task status",
            enum=["new", "in progress", "completed", "postponed"],
            example="in progress",
        ),
    },
)
update_task_fields = Model(
    "Update task model",
    {
        "title": fields.String(
            description="Task title", example="Changes title", min_length=4
        ),
        "description": fields.String(
            description="Task description", example="Changed description", min_length=4
        ),
        "status": fields.String(
            description="Task status",
            enum=["new", "in progress", "completed", "postponed"],
            example="completed",
        ),
    },
)


brief_task_fields = Model(
    "Task brief model", {"id": fields.Integer(), "title": fields.String()}
)
