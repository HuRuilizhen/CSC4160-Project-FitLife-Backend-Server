from backend_app import create_app
from backend_app.config import Config
from flask_cors import CORS
import os

app = create_app()

if __name__ == "__main__":
    os.makedirs(os.path.expanduser(Config.AVATARS_DIR), exist_ok=True)
    os.makedirs(os.path.expanduser(Config.PICTURES_DIR), exist_ok=True)
    CORS(app)
    app.run(debug=True, host="0.0.0.0", port=5004)
