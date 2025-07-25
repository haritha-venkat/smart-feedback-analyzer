import streamlit as st
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
from transformers import pipeline

# Load model only once using Streamlit cache
@st.cache_resource
def load_sentiment_model():
    return pipeline("sentiment-analysis")

# This line is **super important**
sentiment_model = load_sentiment_model()


import os
MONGO_URI = os.getenv("MONGO_URI")
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


st.header("📝 Try Your Own Review!")

user_input = st.text_area("Type your review here 👇", "")

if st.button("🔍 Submit"):
    if user_input.strip() == "":
        st.warning("Please enter a review first!")
    else:
        result = sentiment_model(user_input)[0]
        label = result['label']
        score = result['score']

        if label == "POSITIVE":
            st.success(f"🙂 Sentiment: Positive ({score:.2f})")
        elif label == "NEGATIVE":
            st.error(f"🙁 Sentiment: Negative ({score:.2f})")
        else:
            st.info(f"😐 Sentiment: Neutral-ish ({score:.2f})")


from transformers import pipeline
import streamlit as st

# Load sentiment pipeline
@st.cache_resource  # makes it fast after first run
def load_sentiment_model():
    return pipeline("sentiment-analysis")

sentiment_model = load_sentiment_model()
