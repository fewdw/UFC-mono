from flask import Flask
from flask_cors import CORS

from src.Card.CardController import card
from src.Events.EventsController import events

app = Flask(__name__)
CORS(app)
app.register_blueprint(events, url_prefix="/events")
app.register_blueprint(card, url_prefix="/card")


@app.route("/")
def home():
    return "Stats Service Running!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
