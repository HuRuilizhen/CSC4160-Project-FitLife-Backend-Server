from . import db
from .models import (
    User,
)
from .config import Config

import os
import random
import datetime
import json

import logging
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
    except IntegrityError as ie:
        db.session.rollback()  # Rollback in case of an error
        if "users_email_key" in str(ie):  # Check for unique email constraint violation
            raise ValueError("Email already exists") from ie
        elif "users_username_key" in str(
            ie
        ):  # Check for unique username constraint violation
            raise ValueError("Username already exists") from ie
        else:
            logger.error(f"An unexpected IntegrityError occurred: {str(ie)}")
            raise  # Re-raise the exception if it's another type of integrity error

    except SQLAlchemyError as se:
        db.session.rollback()  # Ensure session is clean after any other SQLAlchemy exception
        logger.error(f"A SQLAlchemy error occurred: {str(se)}")
        raise  # Re-raise the exception to be handled by the caller

    except Exception as e:
        db.session.rollback()  # Ensure session is clean after any other exception
        logger.error(f"An unexpected error occurred while creating user: {str(e)}")
        raise  # Re-raise the exception to be handled by the caller


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
        user.change_username(username)
    if password_hash is not None:
        user.change_password(password_hash)
    if avatar is not None:
        if user.avatar != Config.AVATAR_DEFAULT:
            os.remove(os.path.join(os.path.expanduser(Config.AVATARS_DIR), user.avatar))
        user.change_avatar(avatar)
    if email is not None:
        user.change_email(email)
    return user
