from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from backend_app.models import User, Post
from backend_app.utils import update_post


class PostUpdateResource(Resource):
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
        parser.add_argument("post_id", required=True, type=int, location="form")
        parser.add_argument("title", required=True, location="form")
        parser.add_argument("summary", required=True, location="form")
        parser.add_argument("content", required=True, location="form")
        data = parser.parse_args()

        post_id = data.get("post_id")
        title = data.get("title")
        summary = data.get("summary")
        content = data.get("content")

        post: Post = Post.query.filter_by(id=post_id).first()
        if current_user.id != post.user_id:
            response = {
                "is_valid": False,
                "message": "Not authorized",
            }
            return response

        print(post_id, title, summary, content)

        try:
            update_post(
                post_id=post_id,
                title=title,
                summary=summary,
                content=content,
            )
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
