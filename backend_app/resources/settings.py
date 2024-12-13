from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from backend_app.models import User
from backend_app.utils_db import modify_user
from backend_app.config import Config
import werkzeug
import datetime
import hashlib
import os


class SettingsResource(Resource):
    @jwt_required()
    def post(self):
        current_user_email = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument("email", required=False, location="form")
        parser.add_argument("username", required=False, location="form")
        parser.add_argument("password", required=True, location="form")
        parser.add_argument("new_password", required=False, location="form")
        parser.add_argument(
            "avatar",
            required=False,
            type=werkzeug.datastructures.FileStorage,
            location="files",
        )
        data = parser.parse_args()

        new_email = data["email"]
        new_username = data["username"]
        new_password = data["new_password"]
        avatar_name = None
        if data["avatar"] is not None:
            pad = current_user_email + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            pad = hashlib.sha256(pad.encode("utf-8")).hexdigest()
            avatar_name = f"{pad}.{data['avatar'].filename.split('.')[-1]}"
            data["avatar"].save(
                os.path.join(os.path.expanduser(Config.AVATARS_DIR), avatar_name)
            )

        try:
            current_user: User = User.query.filter_by(email=current_user_email).first()
        except:
            current_user = None

        if current_user is None:
            response = {
                "is_valid": False,
                "message": "User not found",
            }
            return response

        if data["password"] != current_user.password_hash:
            response = {
                "is_valid": False,
                "message": "Invalid credentials",
            }
            return response

        try:
            modify_user(
                user_id=current_user.id,
                username=new_username,
                password_hash=new_password,
                email=new_email,
                avatar=avatar_name,
            )
        except:
            response = {
                "is_valid": False,
                "message": "Error updating settings",
            }
            return response

        response = {
            "is_valid": True,
            "message": "Settings successfully updated",
        }
        return response
