import json
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(page_title="API Monitoring Dashboard", layout="wide")

# Constants for anomaly detection
RESPONSE_TIME_THRESHOLD = 1000  # ms
ERROR_STATUS_CODES = {500, 503, 400}

# Upload log file
st.title("📊 API Monitoring & Anomaly Detection")
uploaded_file = st.file_uploader("Upload your JSON log file", type=["json"])

if uploaded_file:
    # Read JSON file
    logs = json.load(uploaded_file)
    df = pd.DataFrame(logs)

    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Detect anomalies
    anomalies = df[(df["response_time"] > RESPONSE_TIME_THRESHOLD) | (df["status_code"].isin(ERROR_STATUS_CODES))]

    # Show anomalies count
    st.sidebar.header("📌 Anomaly Summary")
    st.sidebar.write(f"🔴 **Total Anomalies:** {len(anomalies)}")
    st.sidebar.write(f"⚠️ **Slow Responses (>1000ms):** {len(df[df['response_time'] > RESPONSE_TIME_THRESHOLD])}")
    st.sidebar.write(f"❌ **Error Status Codes:** {len(df[df['status_code'].isin(ERROR_STATUS_CODES)])}")

    # Show logs table
    st.subheader("📂 Uploaded Logs Preview")
    st.dataframe(df.head())

    # Visualization - Response Time Distribution
    st.subheader("📊 API Response Time Distribution")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df["response_time"], bins=20, kde=True, color="blue", ax=ax)
    ax.axvline(x=RESPONSE_TIME_THRESHOLD, color='red', linestyle='--', label="Threshold (1000ms)")
    ax.set_title("Response Time Distribution")
    ax.set_xlabel("Response Time (ms)")
    ax.set_ylabel("Frequency")
    ax.legend()
    st.pyplot(fig)

    # Visualization - Error Status Codes
    error_counts = df[df["status_code"].isin(ERROR_STATUS_CODES)]["status_code"].value_counts()
    if not error_counts.empty:
        st.subheader("🚨 Error Status Code Frequency")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x=error_counts.index, y=error_counts.values, palette="Reds", ax=ax)
        ax.set_title("Error Status Codes")
        ax.set_xlabel("HTTP Status Code")
        ax.set_ylabel("Count")
        st.pyplot(fig)
    else:
        st.write("✅ No major error codes found in the logs.")

    # Visualization - Response Time Over Time
    st.subheader("⏳ API Response Time Over Time")
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(x=df["timestamp"], y=df["response_time"], marker="o", color="green", ax=ax)
    ax.axhline(y=RESPONSE_TIME_THRESHOLD, color='red', linestyle='--', label="Threshold (1000ms)")
    ax.set_title("Response Time Over Time")
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Response Time (ms)")
    ax.legend()
    st.pyplot(fig)

    # Display detected anomalies
    if not anomalies.empty:
        st.subheader("🚨 Anomaly Log")
        st.dataframe(anomalies)

