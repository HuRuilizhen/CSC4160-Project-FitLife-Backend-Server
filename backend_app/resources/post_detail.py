from flask_restful import Resource
from flask import request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from backend_app.models import User
from backend_app.utils_db import fetch_post_by_id, fetch_comments


class PostDetailResource(Resource):
    @jwt_required()
    def get(self):
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

        try:
            post_id = request.args.get("id")
            post = fetch_post_by_id(post_id)
            comments = fetch_comments(post_id)
        except:
            response = {
                "is_valid": False,
                "message": "Post not found",
            }
            return response

        response = {
            "is_valid": True,
            "post": post,
            "comments": comments,
        }
        return response
