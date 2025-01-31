import os
from pymongo import MongoClient
from datetime import date


class Database:
    def __init__(self):
        mongo_uri = os.environ.get("MONGO_URI")
        self.client = MongoClient(mongo_uri)
        self.db = self.client["stats-db"]

    def events(self):
        return self.db["events"]

    def info(self):
        return self.db["info"]


database = Database()
