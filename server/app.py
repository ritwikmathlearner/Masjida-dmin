from flask import Flask
from dotenv import load_dotenv
from src.routes import Route
from src.db import DB

app: Flask = Flask(__name__)

load_dotenv()

DB().connect()
Route(app).load()

if __name__ == "__main__":
    app.run(debug=True)