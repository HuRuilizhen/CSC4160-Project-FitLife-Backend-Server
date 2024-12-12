from . import db
from .models import User, Post, Comment, DaySummary, ActivityRecord
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


def fetch_post_by_user(user_id: int, datetime: datetime) -> list:
    posts = (
        Post.query.filter_by(user_id=user_id)
        .order_by(Post.created_at.desc())
        .limit(3)
        .all()
    )
    posts_ = []
    for post in posts:
        post: Post
        posts_.append(
            {
                "id": post.id,
                "title": post.title,
                "author": post.user.username,
                "author_avatar_url": Config.API_PREFIX
                + Config.AVATARS_URL
                + post.user.avatar,
                "summary": post.summary,
                "image_url": (
                    Config.API_PREFIX + Config.PICTURES_URL + post.image_url
                    if post.image_url is not None
                    else None
                ),
                "date": post.created_at.strftime("%Y-%m-%d"),
            }
        )
    return posts_


def fetch_activities(user_id: int, datetime: datetime) -> dict:
    recentActivities = (
        ActivityRecord.query.filter_by(user_id=user_id)
        .order_by(ActivityRecord.date.desc())
        .limit(5)
        .all()
    )
    recentActivities_ = []
    for activity in recentActivities:
        activity: ActivityRecord
        recentActivities_.append(
            {
                "id": activity.id,
                "activity_type": activity.activity_type,
                "duration": activity.duration,
                "calories_burned": activity.calories_burned,
                "description": f"{activity.activity_type} for {activity.duration} minutes burned {activity.calories_burned} calories on {activity.date.strftime('%Y-%m-%d')}",
                "date": activity.date.strftime("%Y-%m-%d"),
            }
        )
    return recentActivities_


def fetch_dashboard(user_id: int) -> dict:
    userCaloriesBurned = None
    userCaloriesConsumed = None
    today = datetime.datetime.now().date()
    daySummary: DaySummary = DaySummary.query.filter_by(
        user_id=user_id, date=today
    ).first()

    if daySummary is not None:
        userCaloriesBurned = daySummary.activity_summary
        userCaloriesConsumed = daySummary.diet_summary

    return {
        "userCaloriesBurned": userCaloriesBurned,
        "userCaloriesConsumed": userCaloriesConsumed,
        "posts": fetch_post_by_user(user_id, datetime.datetime.now()),
        "recentActivities": fetch_activities(user_id, datetime.datetime.now()),
    }


def create_post(
    user_id: int, title: str, summary: str, content: str, image_url: str
) -> Post:
    post = Post(
        user_id=user_id,
        title=title,
        summary=summary,
        content=content,
        image_url=image_url,
    )
    db.session.add(post)
    db.session.commit()
    return post


def fetch_post(page: int = 1, per_page: int = 10) -> list:
    posts = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=per_page
    )
    posts_ = []
    for post in posts:
        post: Post
        posts_.append(
            {
                "id": post.id,
                "title": post.title,
                "author": post.user.username,
                "author_avatar_url": Config.API_PREFIX
                + Config.AVATARS_URL
                + post.user.avatar,
                "summary": post.summary,
                "image_url": (
                    Config.API_PREFIX + Config.PICTURES_URL + post.image_url
                    if post.image_url is not None
                    else None
                ),
                "date": post.created_at.strftime("%Y-%m-%d"),
            }
        )
    return posts_


def fetch_post_by_id(post_id: int) -> Post:
    post = Post.query.filter_by(id=post_id).first()
    post_ = {
        "id": post.id,
        "title": post.title,
        "author": post.user.username,
        "author_id": post.user.id,
        "author_avatar_url": Config.API_PREFIX + Config.AVATARS_URL + post.user.avatar,
        "summary": post.summary,
        "content": post.content,
        "image_url": (
            Config.API_PREFIX + Config.PICTURES_URL + post.image_url
            if post.image_url is not None
            else None
        ),
        "date": post.created_at.strftime("%Y-%m-%d"),
    }
    return post_


def fetch_comments(post_id: int) -> list:
    comments = Comment.query.filter_by(post_id=post_id).all()
    comments_ = []
    for comment in comments:
        comment: Comment
        comments_.append(
            {
                "id": comment.id,
                "author": comment.user.username,
                "author_avatar_url": Config.API_PREFIX
                + Config.AVATARS_URL
                + comment.user.avatar,
                "content": comment.content,
                "date": comment.created_at.strftime("%Y-%m-%d"),
            }
        )
    return comments_


def create_comment(user_id: int, post_id: int, content: str) -> Comment:
    comment = Comment(
        user_id=user_id,
        post_id=post_id,
        content=content,
    )
    db.session.add(comment)
    db.session.commit()
    return comment
