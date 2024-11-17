from . import db
from .config import Config
import datetime
import hashlib


class User(db.Model):
    __tablename__ = "users"

    id: int = db.Column(db.Integer, primary_key=True)
    avatar: str = db.Column(db.Integer, nullable=False, default=Config.AVATAR_DEFAULT)
    email: str = db.Column(db.String(120), unique=True, nullable=False)
    username: str = db.Column(db.String(80), unique=True, nullable=False)
    password_hash: str = db.Column(db.String(120), nullable=True)

    def __init__(
        self,
        email: str,
        username: str,
        password_hash: str,
    ) -> None:
        self.email = email
        self.username = username
        self.password_hash = password_hash

    def set_password(self, password: str) -> None:
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password_hash: str) -> bool:
        return self.password_hash == password_hash

    def change_email(self, new_email: str) -> bool:
        try:
            self.email = new_email
            db.session.commit()
            return True
        except:
            return False

    def change_username(self, new_username: str) -> bool:
        self.username = new_username
        db.session.commit()
        return True

    def change_password(self, new_password_hash: str) -> bool:
        self.password_hash = new_password_hash
        db.session.commit()
        return True

    def change_avatar(self, new_avatar: str) -> bool:
        self.avatar = new_avatar
        db.session.commit()
        return True

    def __repr__(self) -> str:
        return f"<User {self.username}>"
