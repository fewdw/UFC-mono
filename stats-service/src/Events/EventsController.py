from flask import Blueprint, jsonify

from src.Events.EventsService import EventService

events = Blueprint("events", __name__)

event_service = EventService()


@events.route("/upcoming", methods=["GET"])
def get_upcoming_events():
    return jsonify(event_service.get_upcoming_events()), 200


@events.route("/past", methods=["GET"])
def get_past_events():
    return jsonify(event_service.get_past_events()), 200
