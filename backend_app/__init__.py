from flask import Flask, send_from_directory
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

from .extensions import db, jwt
from . import resources
from .config import Config


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    api = Api(app)
    api.add_resource(resources.LoginResource, "/api/login")
    api.add_resource(resources.RegisterResource, "/api/register")
    api.add_resource(resources.TokenRefreshResource, "/api/token-refresh")
    api.add_resource(resources.TokenCheckResource, "/api/token-check")

    @app.route(f"{Config.AVATARS_URL}<path:filename>")
    def get_avatar_file(filename: str):
        AVATARS_DIR = os.path.expanduser(Config.AVATARS_DIR)
        return send_from_directory(AVATARS_DIR, filename)

    @app.route(f"{Config.PICTURES_URL}<path:filename>")
    def get_picture_file(filename: str):
        PICTURES_DIR = os.path.expanduser(Config.PICTURES_DIR)
        return send_from_directory(PICTURES_DIR, filename)

    return app
