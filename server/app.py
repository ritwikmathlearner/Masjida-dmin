from flask import Flask
from dotenv import load_dotenv
from src.routes import Route
from src.db import DB
from src.services.mail import mailService

app: Flask = Flask(__name__)

load_dotenv()

DB().connect()
Route(app).load()
app.config['TESTING'] = False
mailService.configure(app)


if __name__ == "__main__":
    app.run(debug=True)