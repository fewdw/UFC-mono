from datetime import date, datetime

from flask import jsonify

from src.Scrape.FightCardInfo import scrape_fight_card
from src.database import database


class CardService:
    def __init__(self):
        pass

    def get_card_info(self, card_link):
        self.fix_card(card_link)
        return database.card().find_one({"event_link": card_link}, {"_id": 0})

    def fix_card(self, card_link):
        last_scrape = database.info().find_one({"name": "card_last_scraped", "event_link": card_link}, {"_id": 0})

        if last_scrape is None:
            database.card().insert_one(scrape_fight_card(card_link))
            database.info().insert_one({"name": "card_last_scraped", "date": str(date.today()), "event_link": card_link})

        elif self.older_than_5(last_scrape["date"]):

            event = database.events().find_one({"event_link": card_link},{"_id": 0})

            if event and event.get("event_happened"):
                return

            scraped_data = scrape_fight_card(card_link)
            database.card().update_one({"event_link": card_link},{"$set": scraped_data})
            database.info().update_one({"name": "card_last_scraped", "event_link": card_link},{"$set": {"date": str(date.today())}})

    def older_than_5(self, date_str):
        last_date = datetime.strptime(date_str, "%Y-%m-%d")
        return (datetime.now() - last_date).days > 4
