import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)

db = client["github_webhooks"]
actions_collection = db["actions"]


def save_webhook_data(payload):
    """
    Save incoming webhook payload into MongoDB
    """
    return actions_collection.insert_one(payload)


def fetch_latest_actions(limit=10):
    """
    Fetch latest webhook actions for UI polling
    """
    actions = actions_collection.find(
        {},
        {"_id": 0}
    ).sort("timestamp", -1).limit(limit)

    return list(actions)
