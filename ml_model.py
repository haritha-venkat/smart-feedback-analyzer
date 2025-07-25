from pymongo import MongoClient
from textblob import TextBlob

import os
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client["feedback_db"]
collection = db["feedbacks_amazon"]


def get_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"


count = 0
for doc in collection.find({"sentiment": {"$exists": False}}):
    sentiment = get_sentiment(doc["feedback"])
    collection.update_one(
        {"_id": doc["_id"]},
        {"$set": {"sentiment": sentiment}}
    )
    count += 1
    if count % 1000 == 0:
        print(f" Processed {count} reviews...")

print(f"\n Sentiment analysis complete for {count} reviews!")
