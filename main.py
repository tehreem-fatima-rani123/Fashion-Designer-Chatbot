# main.py (Antique Fashion Designer Chatbot)
import streamlit as st
from gemini_model import get_response, get_image_response
import time
from streamlit.components.v1 import html

# --- Page Config ---
st.set_page_config(
    page_title="Ai Chatbot",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for Antique Design & Animations ---
st.markdown("""
<style>
/* Base Vintage Styling */
:root {
    --vintage-gold: #D4AF37;
    --antique-brass: #C19A6B;
    --parchment: #F8F4E6;
    --aged-paper: #E8DFCA;
    --deep-burgundy: #800020;
    --vintage-ink: #3D2B1F;
}

body {
    background: url('https://i.imgur.com/YbBz8aB.jpg') no-repeat center center fixed;
    background-size: cover;
    font-family: 'Old Standard TT', serif;
    color: var(--vintage-ink);
}

/* 3D Chat Containers */
.stChatMessage {
    border-radius: 12px !important;
    box-shadow: 
        0 8px 16px rgba(0,0,0,0.25),
        0 2px 4px rgba(0,0,0,0.22),
        inset 0 -3px 0 rgba(0,0,0,0.1);
    transform: perspective(1000px) rotateY(5deg);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    margin-bottom: 2rem !important;
    border: 2px solid var(--vintage-gold) !important;
    background: linear-gradient(145deg, #f9f5e9, #e8dfca) !important;
}

.stChatMessage:hover {
    transform: perspective(1000px) rotateY(0deg) translateY(-5px);
    box-shadow: 
        0 12px 24px rgba(0,0,0,0.3),
        0 4px 8px rgba(0,0,0,0.25),
        inset 0 -3px 0 rgba(0,0,0,0.15);
}

/* User Messages */
[data-testid="stChatMessage"]:has(.user) {
    border-left: 6px solid var(--deep-burgundy) !important;
    background: linear-gradient(145deg, #f0e6d8, #e1d4bb) !important;
}

/* Assistant Messages */
[data-testid="stChatMessage"]:has(.assistant) {
    border-left: 6px solid var(--vintage-gold) !important;
}

/* Typing Animation */
@keyframes vintageTypewriter {
    from { width: 0; }
    to { width: 100%; }
}

@keyframes blinkCaret {
    from, to { border-color: transparent }
    50% { border-color: var(--vintage-gold); }
}

.typewriter h1 {
    overflow: hidden;
    border-right: .15em solid var(--vintage-gold);
    white-space: nowrap;
    margin: 0 auto;
    letter-spacing: .15em;
    animation: 
        vintageTypewriter 3.5s steps(40, end),
        blinkCaret .75s step-end infinite;
}

/* Vintage Input */
.stTextInput>div>div>input {
    background: var(--aged-paper) !important;
    border: 2px solid var(--antique-brass) !important;
    border-radius: 25px !important;
    padding: 15px 20px !important;
    font-size: 1.1rem !important;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.1) !important;
    transition: all 0.3s ease;
}

.stTextInput>div>div>input:focus {
    border-color: var(--vintage-gold) !important;
    box-shadow: 0 0 8px rgba(212, 175, 55, 0.6) !important;
}

/* Image Frames */
.stImage>img {
    border: 12px solid transparent !important;
    padding: 10px !important;
    background: 
        linear-gradient(var(--aged-paper), var(--aged-paper)) padding-box,
        repeating-linear-gradient(
            45deg,
            var(--vintage-gold) 0,
            var(--vintage-gold) 10px,
            var(--antique-brass) 10px,
            var(--antique-brass) 20px
        ) border-box !important;
    box-shadow: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23) !important;
    transform: perspective(1500px) rotateY(10deg);
    transition: transform 1s ease;
}

.stImage>img:hover {
    transform: perspective(1500px) rotateY(0deg);
}

/* Fade-in Animation */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.stChatMessage {
    animation: fadeIn 0.8s ease-out;
}

/* Header Styling */
.stApp>header {
    background-color: transparent !important;
}

h1 {
    font-family: 'Playfair Display', serif !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    position: relative;
    display: inline-block;
}

h1:after {
    content: "";
    position: absolute;
    bottom: -10px;
    left: 0;
    width: 100%;
    height: 3px;
    background: linear-gradient(to right, transparent, var(--vintage-gold), transparent);
}

/* Button Styling */
.stButton>button {
    background: linear-gradient(to right, #8e6e53, #a67c52) !important;
    border: none !important;
    border-radius: 30px !important;
    color: white !important;
    padding: 12px 24px !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
    border: 2px solid #6b4f37 !important;
}

.stButton>button:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.25);
    background: linear-gradient(to right, #a67c52, #c19a6b) !important;
}

/* Scrollbar Styling */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: var(--aged-paper);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: var(--antique-brass);
    border-radius: 10px;
    border: 2px solid var(--aged-paper);
}

::-webkit-scrollbar-thumb:hover {
    background: var(--vintage-gold);
}
</style>
""", unsafe_allow_html=True)

# --- Font Imports ---
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Old+Standard+TT:wght@400;700&family=Playfair+Display:wght@700;800&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

# --- Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.last_interaction = 0

# --- Animated Header ---
st.markdown("""
<div class="typewriter">
    <h1>👗 Fashion Designer AI Chatbot</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("### Your personal AI-powered fashion assistant! 💬=", unsafe_allow_html=True)
st.markdown("---")

# --- Sidebar for Vintage Controls ---

# --- Chat Container ---
chat_container = st.container()

# --- Chat Input with Vintage Style ---
with st.container():
    prompt = st.chat_input("Consult the fashion archives...", key="vintage_input")
    
    if prompt:
        # Add user message
        st.session_state.chat_history.append({"role": "user", "type": "text", "message": prompt})
        st.session_state.last_interaction = time.time()
        
        # Get AI response
        with st.spinner("Consulting fashion archives..."):
            result = get_response(prompt)
            
            # Simulate vintage typing delay
            time.sleep(1.5)
            
            # Text response
            if result.get("text"):
                st.session_state.chat_history.append(
                    {"role": "assistant", "type": "text", "message": result["text"]}
                )
            
            # Image response
            if result.get("image"):
                st.session_state.chat_history.append(
                    {"role": "assistant", "type": "image", "message": result["image"]}
                )

# --- Render Chat with Animation Effects ---
with chat_container:
    for i, chat in enumerate(st.session_state.chat_history):
        # Add slight delay between messages
        time.sleep(0.1) if i > 0 else None
        
        with st.chat_message(chat["role"]):
            if chat["type"] == "text":
                st.markdown(f"<div style='font-size: 1.1rem; line-height: 1.6;'>{chat['message']}</div>", 
                           unsafe_allow_html=True)
            elif chat["type"] == "image":
                st.image(chat["message"], use_column_width=True)

# --- Vintage Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; font-family: 'Old Standard TT'; color: red;">
    <p style="letter-spacing: 2px; font-size: 0.6rem;"></p>
    <p style="font-size: 1rem; opacity: 0.7;">Made By Tehreem Fatima</p>
</div>
""", unsafe_allow_html=True)

# --- Auto-scroll JavaScript ---
html(
    f"""
    <script>
        // Auto-scroll to bottom
        window.addEventListener('load', function() {{
            setTimeout(function() {{
                window.scrollTo(0, document.body.scrollHeight);
            }}, 300);
        }});
        
        // Scroll to new messages
        let lastInteraction = {st.session_state.last_interaction};
        window.addEventListener('load', function() {{
            setInterval(function() {{
                if (lastInteraction !== {st.session_state.last_interaction}) {{
                    lastInteraction = {st.session_state.last_interaction};
                    window.scrollTo(0, document.body.scrollHeight);
                }}
            }}, 100);
        }});
    </script>
    """,
    height=0,
)
