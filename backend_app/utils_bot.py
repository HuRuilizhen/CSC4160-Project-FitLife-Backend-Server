import dashscope
import json
import os
import re

from backend_app.config import Config, BOT_TYPE, PROMPT_PATH


def get_prompt(bot_type: str) -> str:
    STATIC_PROMPT_DIR = os.path.join(
        os.path.abspath(os.curdir), Config.STATIC_PROMPT_DIR
    )
    if bot_type == BOT_TYPE.DIET_WORD:
        path = os.path.join(STATIC_PROMPT_DIR, PROMPT_PATH.DIET_WORD)
    elif bot_type == BOT_TYPE.DIET_PHOTO:
        path = os.path.join(STATIC_PROMPT_DIR, PROMPT_PATH.DIET_PHOTO)
    elif bot_type == BOT_TYPE.ACTIVITY_WORD:
        path = os.path.join(STATIC_PROMPT_DIR, PROMPT_PATH.ACTIVITY_WORD)
    else:
        raise ValueError(f"Unknown bot type: {bot_type}")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def get_dict(content: str) -> dict:
    match = re.search(r"\{.*?\}", content, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError as e:
            print("Failed to decode JSON:", e)
    else:
        raise ValueError("No JSON object found in the text.")


def create_activity_record_bot(note):
    dashscope.api_key = Config.BOT_API_KEY
    prompt = get_prompt(BOT_TYPE.ACTIVITY_WORD)

    messages = [
        {
            "role": "system",
            "content": prompt,
        },
        {"role": "user", "content": note},
    ]
    response = dashscope.Generation.call(
        model="qwen-plus",
        messages=messages,
        result_format="message",
    )

    content = response["output"]["choices"][0]["message"]["content"]
    return get_dict(content)
