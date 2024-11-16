from flask_restful import Resource, reqparse
from backend_app.models import User
from backend_app.config import Config
from backend_app.utils import create_user


class RegisterResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", required=True)
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)
        data = parser.parse_args()

        try:
            create_user(
                email=data["email"],
                username=data["username"],
                password_hash=data["password"],
            )
        except:
            return {"message": "Email already exists", "is_valid": False}

        return {"message": "User successfully created", "is_valid": True}, 201
