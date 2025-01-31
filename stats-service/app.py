from flask import Flask
from flask_cors import CORS

from src.Card.CardController import card
from src.Stats.EventsController import events

app = Flask(__name__)
app.register_blueprint(events, url_prefix="/stats")
app.register_blueprint(card, url_prefix="/card")
CORS(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
