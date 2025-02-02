from flask import Blueprint

from src.Narrative.NarrativeService import NarrativeService

narrative = Blueprint("narrative", __name__)

narrative_service = NarrativeService()

@narrative.route("/")
def get_narrative():
    return narrative_service.hi()