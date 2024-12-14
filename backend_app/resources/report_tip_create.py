from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend_app.models import User
from backend_app.utils_db import create_health_report, fetch_activities, fetch_diets
from backend_app.utils_bot import create_tips_bot_word
from backend_app.config import LIMITS


class ReportTipCreateResource(Resource):
    @jwt_required()
    def post(self):
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

        diet_records = fetch_diets(current_user.id, LIMITS.MAX_TIP_RECORDS)
        activity_records = fetch_activities(current_user.id, LIMITS.MAX_TIP_RECORDS)

        bot_result = create_tips_bot_word(diet_records, activity_records)

        try:
            tip = create_health_report(current_user.id, bot_result)
        except:
            response = {
                "is_valid": False,
                "message": "Error creating tip",
            }
            return response

        response = {
            "is_valid": True,
            "tip": tip,
        }
        return response
