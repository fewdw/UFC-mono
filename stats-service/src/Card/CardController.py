from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest

from src.Card.CardService import CardService
from src.Scrape.FightCardInfo import scrape_fight_card
from src.Scrape.FightsFromEvents import scrape_fight_links

card = Blueprint("card", __name__)

card_service = CardService()


@card.route("/", methods=["POST"])
def get_card():
    try:
        card_url = request.get_json()['card_url']
    except Exception as e:
        return jsonify({"error": f"could not get the card url, {str(e)}"}), 400

    card_info = card_service.get_card_info(card_url)
    return jsonify(card_info)
