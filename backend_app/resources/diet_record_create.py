from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend_app.models import User
from backend_app.utils_db import create_diet_record
from backend_app.utils_bot import create_diet_record_bot_word


class DietRecordCreateResource(Resource):
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
            "note", type=str, required=True, location="json", help="Note is required"
        )

        try:
            data = parser.parse_args()
        except Exception as e:
            return {"is_valid": False, "message": "Invalid request parameters"}

        note = data.get("note")

        if not note:
            return {"is_valid": False, "message": "Note is a required field."}

        bot_result = create_diet_record_bot_word(note)

        food_name = bot_result.get("food_name")
        quantity = bot_result.get("quantity")
        calories_consumed = bot_result.get("calories_consumed")

        if not food_name or not quantity or not calories_consumed:
            return {"is_valid": False, "message": "Invalid bot response"}

        try:
            create_diet_record(
                user_id=current_user.id,
                food_name=food_name,
                quantity=quantity,
                calories_consumed=calories_consumed,
            )
        except Exception as e:
            return {"is_valid": False, "message": "Error creating diet record"}

        return {"is_valid": True, "message": "Diet record successfully created"}
