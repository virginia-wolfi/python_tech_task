from flask_restx import fields, Model


registration_fields = Model(
    "Registration model",
    {
        "first_name": fields.String(
            required=True, description="User's first name", example="Georges"
        ),
        "last_name": fields.String(description="User's last name", example="Simenon"),
        "username": fields.String(
            required=True,
            max_length=15,
            description="User's username",
            example="maigret",
        ),
        "password": fields.String(
            required=True,
            description="User's password",
            example="123456",
        ),
    },
)

login_fields = Model(
    "Login model",
    {
        "username": fields.String(
            required=True,
            description="User's username",
            example="maigret",
        ),
        "password": fields.String(
            required=True, description="User's password", example="123456"
        ),
    },
)

user_brief_fields = Model(
    "User brief model", {"id": fields.Integer(), "username": fields.String()}
)
