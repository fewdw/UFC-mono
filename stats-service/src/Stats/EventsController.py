from flask import Blueprint

from src.Stats.EventsService import EventService

events = Blueprint("events", __name__)

event_service = EventService()


@events.route("/upcoming", methods=["GET"])
def get_upcoming_events():
    return event_service.get_upcoming_events()

@events.route("/past", methods=["GET"])
def get_past_events():
    return event_service.get_past_events()