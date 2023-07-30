"""Responsible for handling database operations."""
import os
import dotenv
from pymongo.mongo_client import MongoClient

ENV = dotenv.load_dotenv()

client = MongoClient(os.getenv("connectionString"))

db = client.accountTracker

usersToTrack = db.usersToTrack
usersData = db.usersData


class Account():
    """Account class."""

    def __init__(self, user_id):
        self.user_id = user_id

    def start_tracking(self):
        """Starts a 'play session'"""
        results = usersToTrack.find_one({"userId": self.user_id})
        if results is not None:
            return "User already exists"
        usersToTrack.insert_one(
            {
                "userId": self.user_id,
                "tracking": True,
                "playing": False,
                "startedplaying": 0,
            })
        return f"We're now tracking ``{self.user_id}``"

    def get_data(self):
        """Returns account tracking data"""
        results = usersToTrack.find_one({"userId": self.user_id})
        return results

    def get_data_main(self):
        """Returns tracking data."""
        results = usersData.find_one({"userId": self.user_id})
        return results

    def write_data(self, data):
        """Writes account tracking data"""
        usersToTrack.update_one({"userId": self.user_id}, {"$set": data})

    def write_data_main(self, data):
        """Writes tracking data."""
        usersData.update_one({"userId": self.user_id}, {"$set": data}, upsert=True)


def get_all_trackable_users():
    """Returns all users that are currently being tracked."""
    return usersToTrack.find({"tracking": True})
