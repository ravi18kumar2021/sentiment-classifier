import streamlit as st
import requests

st.set_page_config(page_title="Review Classifier", page_icon="📝")
st.title("Review Classifier")

BASE_URL = st.secrets["BASE_URL"]

# Text input
text = st.text_area("Enter text:", height=150)

# Model selection
model = st.radio(
    "Select a model:",
    ("Logistic Regression", "SVM", "DistilBERT")
)

col1, col2 = st.columns(2)

# Placeholder for "Please wait..." message
wait_placeholder = col2.empty()

with col1:
    if st.button("Analyze Sentiment"):
        if not text.strip():
            st.warning("Please enter some text.")
        else:
            # Show "Please wait..." message
            wait_placeholder.text("Please wait...")

            payload = {
                "text": text,
                "model": model
            }

            if model == "Logistic Regression":
                API_PATH = BASE_URL + "/predict_lr"
            elif model == "SVM":
                API_PATH = BASE_URL + "/predict_svm"
            elif model == "DistilBERT":
                API_PATH = BASE_URL + "/predict_bert"
            
            try:
                response = requests.post(API_PATH, json=payload)
                data = response.json()

                sentiment = data.get("label", "unknown")
                score = data.get("score", None)

                # Emoji mapping
                emoji_map = {
                    "positive": "😊",
                    "negative": "☹️"
                }

                emoji = emoji_map.get(sentiment, "❓")

                st.subheader("Result")
                st.write(f"**Sentiment:** {sentiment.capitalize()} {emoji}")
                st.write(f"**Score:** {score:.3f}")

            except Exception as e:
                st.error(f"API Error: {e}")
            
            finally:
                # Clear "Please wait..." message
                wait_placeholder.empty()