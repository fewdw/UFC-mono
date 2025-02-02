from src.database import database
class NarrativeService:

    def __init__(self):
        pass


    def hi(self):
        database.collection().insert_one({"hi": "hi"})
        var = database.collection().find_one({"hi": "hi"}, {"_id": 0})
        return str(var)