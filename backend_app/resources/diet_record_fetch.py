from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend_app.models import User
from backend_app.utils_db import fetch_diets
from backend_app.config import LIMITS


class DietRecordFetchResource(Resource):
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
            records = fetch_diets(current_user.id, LIMITS.MAX_DIETS_DASHBOARD)
        except:
            response = {
                "is_valid": False,
                "message": "Error fetching diets",
            }
            return response

        response = {
            "is_valid": True,
            "records": records,
        }
        return response
