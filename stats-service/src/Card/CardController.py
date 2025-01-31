from flask import Blueprint

from src.Scrape.FightCardInfo import scrape_fight_card
from src.Scrape.FightsFromEvents import scrape_fight_links

card = Blueprint("card", __name__)


@card.route("/", methods=["GET"])
def get_card():
    links = scrape_fight_links("http://www.ufcstats.com/event-details/80dbeb1dd5b53e64")
    info = scrape_fight_card(links)
    return info:D

