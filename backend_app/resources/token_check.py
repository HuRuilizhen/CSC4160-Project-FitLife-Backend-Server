from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from backend_app.models import User


class TokenCheckResource(Resource):
    @jwt_required()
    def get(self):
        current_user_name = get_jwt_identity()

        try:
            current_user: User = User.query.filter_by(
                username=current_user_name
            ).first()
        except:
            current_user = None

        if current_user is None:
            response = {
                "is_valid": False,
            }
            return response

        response = {
            "is_valid": True,
        }
        return response
