from flask import Flask
from flask_cors import CORS

from src.Narrative.NarrativeController import narrative

app = Flask(__name__)
CORS(app)

app.register_blueprint(narrative, url_prefix="/narrative")

@app.route("/")
def home():
    return "Narrative Service Running!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
