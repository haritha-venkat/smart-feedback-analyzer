import pandas as pd
from pymongo import MongoClient

import os
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["feedback_db"]
collection = db["feedbacks_amazon"]  

df = pd.read_csv("amazonreviews.csv")

df = df.dropna(subset=["reviews.text"])


df = df[["reviews.text"]].rename(columns={"reviews.text": "feedback"})

data = df.to_dict(orient="records")
collection.insert_many(data)

print(f" Inserted {len(data)} reviews into MongoDB (feedbacks_amazon).")
