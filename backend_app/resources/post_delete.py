from flask_restful import Resource
from flask import request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from backend_app.models import User, Post
from backend_app.utils_db import delete_post


class PostDeleteResource(Resource):
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

        post_id = request.args.get("post_id")
        post: Post = Post.query.filter_by(id=post_id).first()

        if post is None:
            response = {
                "is_valid": False,
                "message": "Post not found",
            }
            return response

        if current_user.id != post.user_id:
            response = {
                "is_valid": False,
                "message": "Not authorized",
            }
            return response

        try:
            delete_post(post_id)
        except Exception as e:
            response = {
                "is_valid": False,
                "message": f"{str(e)}",
            }
            return response

        response = {
            "is_valid": True,
        }
        return response
