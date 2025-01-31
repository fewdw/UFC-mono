from flask import Blueprint

from src.Scrape.UpcomingEvents import get_upcoming_events

stats = Blueprint('stats', __name__)


@stats.route('/upcoming-events', methods=['GET'])
def upcoming_events():
    return get_upcoming_events(), 200