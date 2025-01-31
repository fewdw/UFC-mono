from datetime import datetime, date

from src.Scrape.UpcomingEvents import scrape_upcoming_events
from src.database import database


class EventService:

    def __init__(self):
        pass

    def get_upcoming_events(self):
        self.fix_events()
        return list(database.events().find({"event_happened": False}, {"_id": 0}))

    def get_past_events(self):
        return list(database.events().find({"event_happened": True}, {"_id": 0}))

    """
    CHECK IF EVENTS WERE NEVER SCRAPED
    CHECK IF EVENTS WERE SCRAPED MORE THAN 5 DAYS AGO
    CHECK IF EVENTS HAPPENED
    """

    def fix_events(self):
        last_scrape = database.info().find_one({"name": "events_last_scraped"})

        if last_scrape is None:
            database.info().insert_one({"name": "events_last_scraped", "date": str(date.today())})
            database.events().insert_many(scrape_upcoming_events())

        elif self.older_than_5(last_scrape["date"]):
            database.info().update_one({"name": "events_last_scraped"}, {"$set": {"date": str(date.today())}})

            events = list(database.events().find({}))

            today = datetime.today()

            for event in events:
                event_date = datetime.strptime(event['event_date'], "%B %d, %Y")

                if event_date <= today:
                    database.events().update_one(
                        {"_id": event["_id"]},
                        {"$set": {"event_happened": True}}
                    )
                else:
                    continue

    def older_than_5(self, date):
        date = datetime.strptime(date, "%Y-%m-%d")
        return (datetime.now() - date).days > 5
