from flask import Flask
from flask_cors import CORS

import src.Scrape.Matchup as Matchup

from src.Test.TestController import test_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(test_bp, url_prefix='/test')

@app.route("/")
def home():
    return "Stats Service Online!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
