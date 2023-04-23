from flask import Flask
from dotenv import load_dotenv
from src.routes import Route
from src.db import DB
from src.services.mail import mailService
from flask_cors import CORS

app: Flask = Flask(__name__)
CORS(app)

load_dotenv()

DB().connect()
Route(app).load()
app.config.update(
    TESTING=False,
    SALT='$2b$12$U6ENDJE0edHn3Z4g6Cex/u'
)
mailService.configure(app)


if __name__ == "__main__":
    app.run(debug=True)