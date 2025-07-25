import streamlit as st
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt


MONGO_URI = "mongodb+srv://harithashree0712:hxrithxxz2005@cluster0.sssfs0c.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["feedback_db"]
collection = db["feedbacks_amazon"]


def load_data():
    data = list(collection.find({}, {"_id": 0}))
    return pd.DataFrame(data)

df = load_data()

st.title("📊 Smart Feedback Analyzer — Amazon Reviews")


sentiment_option = st.selectbox("Filter by Sentiment", ["All", "positive", "negative", "neutral"])
if sentiment_option != "All":
    df = df[df["sentiment"] == sentiment_option]


if st.checkbox("Show Data Table"):
    st.dataframe(df, use_container_width=True)


st.subheader("Sentiment Distribution")
sentiment_counts = df["sentiment"].value_counts()
st.bar_chart(sentiment_counts)


st.subheader("Average Review Length")
df["word_count"] = df["feedback"].apply(lambda x: len(x.split()))
st.write(f"📏 Average words per review: {df['word_count'].mean():.2f}")
