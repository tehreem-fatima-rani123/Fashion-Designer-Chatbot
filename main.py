# main.py (Simple Chatbot)
import streamlit as st
from gemini_model import get_response, get_image_response

# --- Page Config ---
st.set_page_config(
    page_title="Fashion Designer Chatbot",
    page_icon="👗",
    layout="wide"
)

# --- Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Title ---
st.title("👗 Fashion Designer AI Chatbot")
st.markdown("Your personal AI-powered fashion assistant! 💬")

# --- Chat Input ---
prompt = st.chat_input("Ask about outfits, trends, or styling advice...")

if prompt:
    # Add user message
    st.session_state.chat_history.append({"role": "user", "type": "text", "message": prompt})

    # Get AI text response
    with st.spinner("Designing your perfect look..."):
        result = get_response(prompt)

        # If AI returned text
        if result.get("text"):
            st.session_state.chat_history.append(
                {"role": "assistant", "type": "text", "message": result["text"]}
            )

        # If AI returned an image URL/path
        if result.get("image"):
            st.session_state.chat_history.append(
                {"role": "assistant", "type": "image", "message": result["image"]}
            )

# --- Render Chat ---
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        if chat["type"] == "text":
            st.markdown(chat["message"])
        elif chat["type"] == "image":
            st.image(chat["message"], use_column_width=True)
