from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend_app.models import User
from backend_app.utils_db import create_activity_record
from backend_app.utils_bot import create_activity_record_bot_word


class ActivityRecordCreateResource(Resource):
    @jwt_required()
    def post(self):
        current_user_email = get_jwt_identity()

        try:
            current_user: User = User.query.filter_by(email=current_user_email).first()
            if not current_user:
                return {"is_valid": False, "message": "User not found"}
        except Exception as e:
            return {"is_valid": False, "message": "Error fetching user"}

        parser = reqparse.RequestParser()
        parser.add_argument(
            "note", type=str, required=True, location="form", help="Note is required"
        )

        try:
            data = parser.parse_args()
        except Exception as e:
            return {"is_valid": False, "message": "Invalid request parameters"}

        note = data.get("note")

        if not note:
            return {"is_valid": False, "message": "Note is a required field."}

        bot_result = create_activity_record_bot_word(note)

        activity_type = bot_result.get("activity_type")
        duration = bot_result.get("duration")
        calories_burned = bot_result.get("calories_burned")

        if not activity_type or not duration or not calories_burned:
            return {"is_valid": False, "message": "Invalid bot response"}

        try:
            create_activity_record(
                user_id=current_user.id,
                activity_type=activity_type,
                duration=duration,
                calories_burned=calories_burned,
            )
        except Exception as e:
            return {"is_valid": False, "message": "Error creating activity record"}

        return {"is_valid": True, "message": "Sport log created successfully."}
