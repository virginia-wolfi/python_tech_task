from flask_restx import Resource, Namespace, marshal
from flask_jwt_extended import create_access_token, current_user, jwt_required, get_jwt
from ..models.user import UserModel
from ..models.blocked_token import TokenBlocklist
from flask import request, jsonify, abort, make_response
from ..operations import save_to_db, delete_from_db
from .api_models.user import registration_fields, login_fields, user_brief_fields
from ..db import db
from datetime import datetime
from datetime import timezone


users = Namespace("Users", description="Users related operations", path="/")


class UserRegister(Resource):
    @users.expect(registration_fields)
    @users.marshal_with(user_brief_fields, envelope="User created")
    @users.doc(
        responses={
            201: "Created",
            400: "Validation error",
        }
    )
    def post(self):
        """Registers new user"""
        input_fields = marshal(request.get_json(), registration_fields)
        if UserModel.find_by_username(input_fields["username"]):
            abort(400, "This username is taken")

        user = UserModel(**input_fields)
        save_to_db(user)
        return user, 201


class UserLogin(Resource):
    @users.expect(login_fields)
    @users.doc(
        responses={
            200: "Success",
            400: "Validation error",
        }
    )
    def post(self):
        """Logs in user
        Copy access_token given in response and paste in Authorization header where applicable in format Bearer JWT
        """
        input_fields = marshal(request.get_json(), login_fields)

        user = UserModel.find_by_username(input_fields["username"])
        password = input_fields["password"]

        if user and user.check_password(password):
            access_token = create_access_token(identity=user)
            return make_response({"access_token": access_token}, 200)

        abort(400, "Wrong username or password")


class UserLogout(Resource):
    @users.doc(
        security="Bearer Auth",
        responses={
            200: "Success",
            401: "Unauthorized",
        },
    )
    @jwt_required()
    def post(self):
        """Logs out user"""
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()
        return make_response(jsonify({"message": "User logged out successfully"}), 200)


class UserProfile(Resource):
    @users.marshal_with(registration_fields, envelope="User's profile")
    @jwt_required()
    @users.doc(
        security="Bearer Auth",
        responses={
            200: "Success",
            401: "Unauthorized",
        },
    )
    def get(self):
        """Shows user's profile"""
        id = current_user.id
        user = db.session.scalars(db.select(UserModel).filter_by(id=id)).first()
        return user, 200

    @jwt_required()
    @users.doc(
        security="Bearer Auth",
        responses={
            200: "Success",
            401: "Unauthorized",
        },
    )
    def delete(self):
        """Deletes user and tasks created by user"""
        user = current_user
        delete_from_db(user)
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()
        return make_response(jsonify({"message": "Profile deleted"}), 200)
