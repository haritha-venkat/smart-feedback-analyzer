import pandas as pd
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://harithashree0712:hxrithxxz2005@cluster0.sssfs0c.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["feedback_db"]
collection = db["feedbacks_amazon"]  

df = pd.read_csv("amazonreviews.csv")

df = df.dropna(subset=["reviews.text"])


df = df[["reviews.text"]].rename(columns={"reviews.text": "feedback"})

data = df.to_dict(orient="records")
collection.insert_many(data)

print(f" Inserted {len(data)} reviews into MongoDB (feedbacks_amazon).")
