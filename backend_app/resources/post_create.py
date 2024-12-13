from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from backend_app.models import User
from backend_app.utils_db import create_post
from backend_app.config import Config
import hashlib, os, datetime


class PostCreateResource(Resource):
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
        parser.add_argument(
            "title",
            type=str,
            required=True,
            location="form",
            help="Title cannot be blank.",
        )
        parser.add_argument(
            "summary",
            type=str,
            required=True,
            location="form",
            help="Summary cannot be blank.",
        )
        parser.add_argument(
            "content",
            type=str,
            required=True,
            location="form",
            help="Content cannot be blank.",
        )
        parser.add_argument(
            "image", type=reqparse.FileStorage, location="files", required=False
        )

        data = parser.parse_args()

        title = data.get("title")
        summary = data.get("summary")
        content = data.get("content")
        image_file = data.get("image")

        if title is None or summary is None or content is None:
            response = {
                "is_valid": False,
                "message": "Title, summary and content cannot be blank.",
            }
            return response

        if image_file is not None:
            pad = current_user_email + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            pad = hashlib.sha256(pad.encode("utf-8")).hexdigest()
            image_name = f"{pad}.{image_file.filename.split('.')[-1]}"
            image_file.save(
                os.path.join(os.path.expanduser(Config.PICTURES_DIR), image_name)
            )

        try:
            create_post(
                user_id=current_user.id,
                title=title,
                summary=summary,
                content=content,
                image_url=(image_name if image_name is not None else None),
            )
        except Exception as e:
            response = {
                "is_valid": False,
                "message": "An error occurred while creating the post.",
            }
            return response

        response = {
            "is_valid": True,
            "message": "Post created successfully.",
        }
        return response
