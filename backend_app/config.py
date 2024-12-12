from datetime import timedelta


class Config:
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = "secret-key"

    JWT_SECRET_KEY = "jwt-secret-key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    API_PREFIX = "/api"

    AVATAR_DEFAULT = "default.jpg"
    STATIC_DIR = "backend_app/static/"

    AVATARS_DIR = "~/mnt/storage/avatars"
    PICTURES_DIR = "~/mnt/storage/pictures"

    AVATARS_URL = "/avatars/"
    PICTURES_URL = "/pictures/"
