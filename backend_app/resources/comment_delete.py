from flask_restful import Resource
from flask import request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from backend_app.models import User, Comment
from backend_app.utils import delete_comment


class CommentDeleteResource(Resource):
    @jwt_required()
    def delete(self):
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

        comment_id = request.args.get("comment_id")
        comment: Comment = Comment.query.filter_by(id=comment_id).first()

        if comment is None:
            response = {
                "is_valid": False,
                "message": "Comment not found",
            }
            return response

        if current_user.id != comment.user_id:
            response = {
                "is_valid": False,
                "message": "Not authorized",
            }
            return response

        try:
            delete_comment(comment_id)
        except:
            response = {
                "is_valid": False,
                "message": "Comment not found",
            }
            return response

        response = {
            "is_valid": True,
        }
        return response
