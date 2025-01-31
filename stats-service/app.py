import os

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from src.Stats.StatsController import stats

load_dotenv()
app = Flask(__name__)
CORS(app)
db_url = os.getenv('SQLALCHEMY_DATABASE_URI')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.register_blueprint(stats, url_prefix='/stats')


@app.route("/", methods=["GET"])
def home():
    return "Stats service online!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
