from flask import Flask, send_from_directory
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

from .extensions import db, jwt
from .config import Config
from . import resources


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    api = Api(app)
    api.add_resource(resources.LoginResource, "/api/login")
    api.add_resource(resources.RegisterResource, "/api/register")
    api.add_resource(resources.SettingsResource, "/api/settings")
    api.add_resource(resources.TokenRefreshResource, "/api/token/refresh")
    api.add_resource(resources.TokenCheckResource, "/api/token/check")
    api.add_resource(resources.DashboardFetchResource, "/api/dashboard/fetch")
    api.add_resource(resources.PostCreateResource, "/api/post/create")
    api.add_resource(resources.PostFetchResource, "/api/post/fetch")
    api.add_resource(resources.PostDetailResource, "/api/post/detail")
    api.add_resource(resources.PostDeleteResource, "/api/post/delete")
    api.add_resource(resources.PostUpdateResource, "/api/post/update")
    api.add_resource(resources.CommentCreateResource, "/api/comment/create")
    api.add_resource(resources.CommentDeleteResource, "/api/comment/delete")
    api.add_resource(resources.DietRecordFetchResource, "/api/diet/fetch")
    api.add_resource(resources.ActivityRecordCreateResource, "/api/activity/create")
    api.add_resource(resources.ActivityRecordFetchResource, "/api/activity/fetch")

    @app.route(f"{Config.API_PREFIX}{Config.AVATARS_URL}<path:filename>")
    def get_avatar_file(filename: str):
        if filename == Config.AVATAR_DEFAULT:
            STATIC_AVATAR_DIR = os.path.join(
                os.path.abspath(os.curdir), Config.STATIC_AVATAR_DIR
            )
            return send_from_directory(STATIC_AVATAR_DIR, filename)
        AVATARS_DIR = os.path.expanduser(Config.AVATARS_DIR)
        return send_from_directory(AVATARS_DIR, filename)

    @app.route(f"{Config.API_PREFIX}{Config.PICTURES_URL}<path:filename>")
    def get_picture_file(filename: str):
        PICTURES_DIR = os.path.expanduser(Config.PICTURES_DIR)
        return send_from_directory(PICTURES_DIR, filename)

    return app
