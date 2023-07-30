import os
import dotenv
import pymongo
from pymongo.mongo_client import MongoClient

env = dotenv.load_dotenv()

client = MongoClient(os.getenv("connectionString"))

db = client.accountTracker

usersToTrack = db.usersToTrack
usersData = db.usersData

