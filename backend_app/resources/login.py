import os
import base64
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
from backend_app.models import User
from backend_app.config import Config


class LoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", required=False)
        parser.add_argument("password", required=False)
        parser.add_argument(
            "usertoken",
            required=False,
        )
        data = parser.parse_args()

        try:
            current_user: User = User.query.filter_by(email=data["email"]).first()
        except:
            current_user = None

        if not current_user:
            response = {
                "message": "User not found",
                "is_valid": False,
            }
            return response

        if not current_user.check_password(data["password"]):
            response = {
                "message": "Invalid credentials",
                "is_valid": False,
            }
            return response

        avatar_base64 = None
        if current_user.avatar:
            if current_user.avatar == Config.AVATAR_DEFAULT:
                AVATARS_DIR = Config.STATIC_DIR
            else:
                AVATARS_DIR = os.path.expanduser(Config.AVATARS_DIR)
            avatar_path = os.path.join(AVATARS_DIR, current_user.avatar)
            with open(avatar_path, "rb") as f:
                avatar_base64 = base64.b64encode(f.read()).decode("utf-8")

        response = {
            "message": f"Login successfully as {current_user.username}",
            "user": {
                "username": current_user.username,
                "avatar_base64": avatar_base64,
            },
            "is_valid": True,
            "access_token": create_access_token(identity=current_user.email),
            "refresh_token": create_refresh_token(identity=current_user.email),
        }
        return response
