from . import db
from .config import Config
import datetime
import hashlib


class User(db.Model):
    __tablename__ = "users"

    id: int = db.Column(db.Integer, primary_key=True)
    avatar: str = db.Column(
        db.String(255), nullable=False, default=Config.AVATAR_DEFAULT
    )
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


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    image_url = db.Column(db.String(255))

    user = db.relationship("User", backref=db.backref("posts", lazy=True))

    def __repr__(self):
        return f"<Post {self.title}>"


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user = db.relationship("User", backref=db.backref("comments", lazy=True))
    post = db.relationship("Post", backref=db.backref("comments", lazy=True))

    def __repr__(self):
        return f"<Comment {self.content[:50]}>"


class ActivityRecord(db.Model):
    __tablename__ = "activity_records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    day_summary_id = db.Column(
        db.Integer, db.ForeignKey("day_summaries.id"), nullable=False
    )
    activity_type = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    calories_burned = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, default=datetime.date.today)

    user = db.relationship("User", backref=db.backref("activities", lazy=True))
    day_summary = db.relationship(
        "DaySummary", backref=db.backref("activities", lazy=True)
    )

    def __repr__(self):
        return f"<Activity {self.activity_type} - {self.duration} minutes>"


class DietRecord(db.Model):
    __tablename__ = "diet_records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    day_summary_id = db.Column(
        db.Integer, db.ForeignKey("day_summaries.id"), nullable=False
    )
    food_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, default=datetime.date.today)

    user = db.relationship("User", backref=db.backref("diet_records", lazy=True))
    day_summary = db.relationship(
        "DaySummary", backref=db.backref("diet_records", lazy=True)
    )

    def __repr__(self):
        return f"<DietRecord {self.food_name} - {self.quantity}g>"


class DaySummary(db.Model):
    __tablename__ = "day_summaries"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    date = db.Column(db.Date, default=datetime.date.today)
    activity_summary = db.Column(db.Text)
    diet_summary = db.Column(db.Text)

    user = db.relationship("User", backref=db.backref("day_summaries", lazy=True))

    def __repr__(self):
        return f"<DaySummary {self.date}>"


class HealthReport(db.Model):
    __tablename__ = "health_reports"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    report_date = db.Column(db.Date, default=datetime.date.today)
    activity_summary = db.Column(db.Text)
    diet_summary = db.Column(db.Text)
    health_advice = db.Column(db.Text)

    user = db.relationship("User", backref=db.backref("health_reports", lazy=True))

    def __repr__(self):
        return f"<HealthReport {self.report_date}>"
