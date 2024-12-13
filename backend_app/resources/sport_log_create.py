from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend_app.models import ActivityRecord, User, db
import datetime
import logging

# 设置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class SportLogCreateResource(Resource):
    @jwt_required()
    def post(self):
        current_user_email = get_jwt_identity()
        logger.info(f"Received request to create sport log for user: {current_user_email}")

        # 获取当前用户
        try:
            current_user = User.query.filter_by(email=current_user_email).first()
            if not current_user:
                logger.warning(f"User not found for email: {current_user_email}")
                return {"is_valid": False, "message": "User not found"}, 404
        except Exception as e:
            logger.error(f"Error fetching user from database: {str(e)}")
            return {"is_valid": False, "message": "Error fetching user"}, 500

        # 解析请求参数
        parser = reqparse.RequestParser()
        parser.add_argument("note", type=str, required=True, location="json", help="Note is required")

        try:
            data = parser.parse_args()
        except Exception as e:
            logger.error(f"Error parsing request arguments: {str(e)}")
            return {"is_valid": False, "message": "Invalid request parameters"}, 400

        note = data.get("note")
        logger.info(f"Parsed request data: note={note}")

        # 检查字段是否为空
        if not note:
            logger.warning("Missing required field: note")
            return {"is_valid": False, "message": "Note is a required field."}, 400
        
        # 接入大模型api分析用户输入的文本记录
        import dashscope
        import os
        import json
        import re

        dashscope.api_key = "sk-b1781e3b50a846109b9667820078c648" 
        messages = [
            {'role': 'user', 'content': """你是一个健康运动分析师。我会告诉你一些与运动相关的描述信息，请用以下严格的格式返回分析结果，不要包含其他多余的解释或内容。格式要求：
            您的运动类型是<运动类型，例如 'running' 或 'cycling'>, 您运动了<运动时长，以分钟为单位，整数，例如 30>分钟,共消耗了约<消耗的卡路里，整数，例如 300>卡路里."""},
            {'role': 'user', 'content': """如果输入的内容与运动无关,则严格输出以下格式：您的表达还不够清晰哦,能否重新描述一下您的运动内容？"""},
            {'role': 'user', 'content': note}
            ]
        response = dashscope.Generation.call(
            api_key=os.getenv('sk-b1781e3b50a846109b9667820078c648'),
            model="qwen-plus",
            messages=messages,
            result_format='message'
            )
        
        # TODO:分析response.content
        print(response)

        # 提取 AI 返回的内容
        ai_content = response["output"]["choices"][0]["message"]["content"]

        # 使用正则表达式提取值
        exercise_type_match = re.search(r"运动类型是(\w+)", ai_content)
        duration_match = re.search(r"运动了(\d+)分钟", ai_content)
        calories_match = re.search(r"消耗了约?(\d+)卡路里", ai_content)

        # 解析提取结果
        if exercise_type_match and duration_match and calories_match:
            exercise_type = exercise_type_match.group(1)
            duration = int(duration_match.group(1))
            calories_text = calories_match.group(1)
        else:
            return {"is_valid": False, "message": "Your expression is not clear enough. Can you describe your exercise content again?"}, 500

        # 构建正则化后的 JSON 数据
        result = {
            "exercise_type": exercise_type,
            "duration": duration,
            "calories": calories_text
        }

        # 存入数据库??

        # try:
        #     new_activity = ActivityRecord(
        #         user_id=current_user.id,
        #         activity_type="Note",  # 用一个固定的 activity_type 表示这是用户输入的文本记录
        #         duration=0,  # 用户未提供时，默认设置为 0
        #         calories_burned=0.0,  # 用户未提供时，默认设置为 0.0
        #         date=datetime.date.today(),  # 使用当前日期
        #         note=note,  # 新增字段，存储用户输入的记录
        #     )
        #     db.session.add(new_activity)
        #     db.session.commit()
        #     logger.info(f"Sport log created successfully for user: {current_user_email}")
        #     return {"is_valid": True, "message": "Sport log created successfully."}, 201
        # except Exception as e:
        #     db.session.rollback()
        #     logger.error(f"Database error while creating sport log: {str(e)}")
        #     return {"is_valid": False, "message": "An error occurred while creating the sport log."}, 500

        return {"is_valid": True, "message": "Sport log created successfully."}, 200