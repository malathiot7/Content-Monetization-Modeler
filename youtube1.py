import streamlit as st
import pickle
import pandas as pd
import numpy as np
from googleapiclient.discovery import build
import requests
import isodate
from urllib.parse import urlparse, parse_qs
from streamlit_option_menu import option_menu
from PIL import Image

print('success')


# Load Models and Scaler

with open("linear_model.pkl", "rb") as f:
    lr = pickle.load(f)
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)
with open("ridge_model.pkl", "rb") as f:
    ridge = pickle.load(f)
with open("lasso_model.pkl", "rb") as f:
    lasso = pickle.load(f)

model_dict = {"Linear Regression": lr, "Ridge Regression": ridge, "Lasso Regression": lasso}


# YouTube API Setup

API_KEY = "your API"

class categoryMap:
    category = {
        "Education": "27",
        "Tech": "28",
        "Music": "10",
        "Entertainment": "24",
        "Gaming": "20",
        "Lifestyle": "22"
    }

def getVideoAnalytics(video_url):
    def extract_video_id(url):
        parsed = urlparse(url)
        if "youtube.com" in parsed.netloc:
            if parsed.path == "/watch":
                return parse_qs(parsed.query).get("v", [None])[0]
            elif "/shorts/" in parsed.path:
                return parsed.path.split("/shorts/")[1].split("?")[0]
        if "youtu.be" in parsed.netloc:
            return parsed.path.lstrip("/").split("?")[0]
        return None

    video_id = extract_video_id(video_url)
    video_stats_url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet,contentDetails&id={video_id}&key={API_KEY}"
    video_data = requests.get(video_stats_url).json()

    if video_data["items"]:
        item = video_data["items"][0]
        stats = item["statistics"]
        snippet = item["snippet"]
        likes = stats.get("likeCount", "0")
        views = stats.get("viewCount", "0")
        comments = stats.get("commentCount", "0")
        date = snippet.get("publishedAt", "")
        details = item["contentDetails"]
        duration = isodate.parse_duration(details["duration"])
        video_length_minutes = round(duration.total_seconds() / 60, 2)
        category_id = snippet.get("categoryId", "")
        channel_id = snippet.get("channelId", "")

        mapCategory = categoryMap.category
        category = [key for key, value in mapCategory.items() if value == category_id]
        if not category:
            category = ["Education"]

        # Get channel subscribers
        channel_url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={API_KEY}"
        channel_data = requests.get(channel_url).json()
        subscribers = channel_data["items"][0]["statistics"].get("subscriberCount", "0")

        video_info = {
            'views': views,
            'likes': likes,
            'comments': comments,
            'watch_time_minutes': 0,
            'video_length_minutes': video_length_minutes,
            'subscribers': subscribers,
            'category': category[0],
            'engagement_rate': 0,
        }

        video_info['watch_time_minutes'] = round((video_length_minutes * int(views)) / 60, 2)
        video_info['month'] = pd.to_datetime(date).month
        video_info['is_weekend'] = 1 if pd.to_datetime(date).weekday() >= 5 else 0

        encode = {'Education': 0, 'Tech': 1, 'Music': 2, 'Entertainment': 3, 'Gaming': 4, 'Lifestyle': 5}
        video_info['category'] = encode[video_info['category']]
        video_info['engagement_rate'] = (int(likes) + int(comments)) / int(views)
        return video_info
    else:
        st.error("Video not found or invalid URL.")
        return None


# Streamlit UI

st.set_page_config(page_title="YouTube Ad Revenue Predictor", page_icon="🎬", layout="wide")
st.title("🎬 YouTube Ad Revenue Prediction App")
st.markdown("Estimate ad revenue for a YouTube video using performance metrics.")

with st.sidebar:
    select = option_menu("Main Menu", ["MODEL SELECTION", "PREDICTION", "ABOUT"], icons=["cpu", "graph-up", "info-circle"])


# MODEL SELECTION PAGE

if select == "MODEL SELECTION":
    st.markdown("### ⚙️ Step 1: Choose a Prediction Model")

   
    model_choice = st.radio(
        "Select a model below:",
        ["Linear Regression", "Ridge Regression", "Lasso Regression"],
        index=0,
        horizontal=False,
    )

    st.markdown("---")
    st.markdown("### 🎥 Step 2: Paste YouTube Video Link")

    
    with st.form('video_form', border=True):
        video_url = st.text_input("Enter the YouTube Video URL:")
        submitted = st.form_submit_button("🔍 Analyze Video")

        if submitted and video_url:
            with st.spinner("Fetching video analytics..."):
                output = getVideoAnalytics(video_url)
        else:
            output = None

    # Video preview
    if video_url:
        st.video(video_url)
    else:
        st.info("ℹ️ Paste a valid YouTube link above to preview the video.")

    st.markdown("---")

    #  Show prediction
    if output is not None:
        st.subheader("📊 Video Information")
        st.dataframe(pd.DataFrame([output]))

        video_df = pd.DataFrame([output])
        video_df_scaled = scaler.transform(video_df)
        model = model_dict[model_choice]
        prediction = model.predict(video_df_scaled)

        st.markdown("---")
        st.markdown("### 💰 Predicted Ad Revenue")
        st.metric(label=f"{model_choice} Prediction (USD)", value=f"${prediction[0]:,.2f}")
   


# PREDICTION PAGE

elif select == "PREDICTION":
    col1, col2 = st.columns(2)
    with col1:
        st.header("Input Video Metrics")
        views = st.number_input("Views", min_value=0)
        likes = st.number_input("Likes", min_value=0.0)
        comments = st.number_input("Comments", min_value=0.0)
        watch_time_minutes = st.number_input("Watch Time (minutes)", min_value=0.0)
        video_length_minutes = st.number_input("Video Length (minutes)", min_value=0.0)
        subscribers = st.number_input("Subscribers", min_value=0)
        category = st.number_input("Category (numeric encoding)", min_value=0)
        engagement_rate = st.number_input("Engagement Rate", min_value=0.0, max_value=1.0, format="%.4f")
        month = st.slider("Upload Month", 1, 12)
        is_weekend = st.selectbox("Uploaded on Weekend?", [0, 1])

        if st.button("Predict Revenue"):
            input_df = pd.DataFrame([[views, likes, comments, watch_time_minutes,
                                    video_length_minutes, subscribers, category,
                                    engagement_rate, month, is_weekend]],
                                    columns=['views', 'likes', 'comments', 'watch_time_minutes',
                                             'video_length_minutes', 'subscribers', 'category',
                                             'engagement_rate', 'month', 'is_weekend'])
            scaled_input = scaler.transform(input_df)
            prediction = lr.predict(scaled_input)[0]
            prediction = max(0, prediction)
            st.success(f"💰 Estimated Ad Revenue: ${prediction:,.2f}")
    
    with col2:
        st.header("How to Use")
        st.markdown("""
        1. Enter your video metrics in the left column.  
        2. Click **Predict Revenue** to get the estimated ad revenue.  
        3. Switch to **MODEL SELECTION** to try Ridge or Lasso models.  
        4. Explore **TOP CHARTS VISUALIZATION** for trends and insights.
        """)
        try:
            st.image(Image.open("image/logo.png"), width=600)
        except:
            st.info("Logo image not found.")


# ABOUT PAGE

elif select == "ABOUT":
    st.header("About the Project")
    st.markdown("""
    **Content Monetization Modeler** helps predict YouTube ad revenue based on video performance metrics.
    
    **Skills & Techniques:**  
    - Regression Models: Linear, Ridge, Lasso  
    - Feature Engineering & EDA  
    - Data Cleaning & Missing Value Handling  
    - Streamlit Web App Deployment  

    **Domain:** Social Media Analytics
    """)

    try:
            st.image(Image.open("image/youtube-analytics.png"), width=600)
    except:

            st.info("Logo image not found.")
