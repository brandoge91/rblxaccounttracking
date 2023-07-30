import os
import dotenv
from pymongo.mongo_client import MongoClient

env = dotenv.load_dotenv()

client = MongoClient(os.getenv("connectionString"))

db = client.accountTracker

usersToTrack = db.usersToTrack
usersData = db.usersData

class account():
    """Dbmanager account class"""
    def __init__(self, userId):
        self.userId = userId

    def startTracking(self):
        results = usersToTrack.find_one({"userId": self.userId})
        if results is not None:
            return "User already exists"
        else:
            usersToTrack.insert_one(
            {
                "userId": self.userId,
                "tracking": True,
                "playing": False,
                "startedplaying": 0,
            })
            return f"We're now tracking ``{self.userId}``"

    def getData(self):
        results = usersData.find_one({"userId": self.userId})
        return results

    def writeData(self, lastLocation, LastOnline, userPresenceType, universeId, hoursPlayed):
        usersData.update_one({"userId": self.userId},{"$set": {"lastLocation": lastLocation, "lastOnline": LastOnline, "userPresenceType": userPresenceType, "universeId": universeId, "hoursPlayed": hoursPlayed}}, upsert=True)
