from flask_restful import Resource
from flask_restful import reqparse
from flask import request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from backend_app.models import User
from backend_app.utils import create_comment


class CommentCreateResource(Resource):
    @jwt_required()
    def post(self):
        current_user_email = get_jwt_identity()

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

        parser = reqparse.RequestParser()
        parser.add_argument("post_id", required=True)
        parser.add_argument("content", required=True)
        data = parser.parse_args()

        post_id = data["post_id"]
        content = data["content"]

        try:
            create_comment(
                user_id=current_user.id,
                post_id=post_id,
                content=content,
            )
        except Exception as e:
            return {"message": f"{str(e)}", "is_valid": False}

        return {"message": "Comment successfully created", "is_valid": True}
