from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from backend_app.models import User
from backend_app.utils_db import fetch_dashboard


class DashboardFetchResource(Resource):
    @jwt_required()
    def get(self):
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

        response = {
            "is_valid": True,
            **fetch_dashboard(current_user.id),
        }
        return response
