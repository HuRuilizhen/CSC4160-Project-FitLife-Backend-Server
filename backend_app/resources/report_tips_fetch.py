from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend_app.models import User
from backend_app.utils_db import fetch_health_reports


class ReportTipsFetchResource(Resource):
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

        try:
            tips = fetch_health_reports(current_user.id)
        except:
            response = {
                "is_valid": False,
                "message": "Error fetching tips",
            }
            return response

        response = {
            "is_valid": True,
            "tips": tips,
        }
        return response
