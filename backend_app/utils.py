from . import db
from .models import (
    User,
)
from .config import Config

import os
import random
import datetime
import json


def create_user(email: str, username: str, password_hash: str) -> User:
    """Create a new user"""
    try:
        user = User(
            email=email,
            username=username,
            password_hash=password_hash,
        )
        db.session.add(user)
        db.session.commit()
        return user
    except:
        raise ValueError("Email already exists")


def delete_user(user_id: int) -> None:
    user: User = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()


def modify_user(
    user_id: int,
    username: str = None,
    password_hash: str = None,
    avatar: str = None,
    email: str = None,
) -> User:
    user: User = User.query.filter_by(id=user_id).first()
    if username is not None:
        user.change_avatar(username)
    if password_hash is not None:
        user.change_avatar(password_hash)
    if avatar is not None:
        user.change_avatar(avatar)
    if email is not None:
        user.change_password(password_hash)
    return user
