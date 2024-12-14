from datetime import timedelta


class Config:
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = "secret-key"

    JWT_SECRET_KEY = "jwt-secret-key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    STATIC_DIR = "backend_app/static/"
    STATIC_AVATAR_DIR = "backend_app/static/avatar/"
    STATIC_PROMPT_DIR = "backend_app/static/prompt/"

    AVATAR_DEFAULT = "default.jpg"

    AVATARS_DIR = "~/mnt/storage/avatars"
    PICTURES_DIR = "~/mnt/storage/pictures"

    API_PREFIX = "/api"
    AVATARS_URL = "/avatars/"
    PICTURES_URL = "/pictures/"

    BOT_API_KEY = "sk-b1781e3b50a846109b9667820078c648"


class BOT_TYPE:
    DIET_WORD = "DIET_WORD"
    DIET_PHOTO = "DIET_PHOTO"
    ACTIVITY_WORD = "ACTIVITY_WORD"
    TIPS_WORD = "TIPS_WORD"


class PROMPT_PATH:
    DIET_WORD = "diet_word.txt"
    DIET_PHOTO = "diet_photo.txt"
    ACTIVITY_WORD = "activity_word.txt"
    TIPS_WORD = "tips_word.txt"


class LIMITS:
    MAX_POSTS_PER_PAGE = 10
    MAX_DIETS_DASHBOARD = 5
    MAX_ACTIVITIES_DASHBOARD = 5
    MAX_POSTS_DASHBOARD = 5
    MAX_LIMIT = 10000
