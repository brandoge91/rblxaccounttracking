import os
import dotenv
from pymongo.mongo_client import MongoClient

env = dotenv.load_dotenv()

client = MongoClient(os.getenv("connectionString"))

db = client.accountTracker

usersToTrack = db.usersToTrack
usersData = db.usersData

class account():
    def __init__(self, UserId):
        self.UserId = UserId

    def startTracking(self):
        results = usersToTrack.find_one({"UserId": self.UserId})
        if results != None:
            return "User already exists"
        else:
            usersToTrack.insert_one({"UserId": self.UserId})
            return f"We're now tracking {self.UserId}"