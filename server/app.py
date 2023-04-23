from flask import Flask, request
from dotenv import load_dotenv
from src.routes import Route
from src.db import DB
from src.services.mail import mailService
from flask_cors import CORS
from src.model.log import LogModel
from datetime import datetime, timezone

app: Flask = Flask(__name__)
CORS(app)

load_dotenv()

DB().connect()
Route(app).load()
app.config.update(
    TESTING=False,
    SALT='$2b$12$L2AV7INnQavIlBKwQIc9je'
)
mailService.configure(app)


if __name__ == "__main__":
    @app.before_request
    def load_user():
        data = request.method == 'POST' and request.json or None
        LogModel().create({
            'http_method': request.method,
            'data': data,
            'ip': request.remote_addr,
            'requested_at': f"{datetime.now(timezone.utc):%Y-%m-%d %H:%M}",
            'timezone': 'UTC',
            'url': request.path
        })
    app.run(debug=True)