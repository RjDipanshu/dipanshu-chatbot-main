import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_message_histories import ChatMessageHistory
from dotenv import load_dotenv
import io

import os

# --------------------------------------------------
# ENV SETUP
# --------------------------------------------------
load_dotenv()

# Streamlit Cloud requires secrets to be accessed via st.secrets if not in os.environ
if "GOOGLE_API_KEY" not in os.environ and "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

if "GOOGLE_API_KEY" not in os.environ:
    st.error("⚠️ GOOGLE_API_KEY not found! Please set it in your environment variables or Streamlit secrets.")
    st.stop()

st.set_page_config(page_title="Syntax Chatbot", page_icon="🤖", layout="centered")

# --------------------------------------------------
# SESSION STATE SETUP
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = ChatMessageHistory()

# --------------------------------------------------
# MODEL
# --------------------------------------------------
try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.7
    )
except Exception as e:
    st.error(f"Failed to initialize model: {e}")
    st.stop()



# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.title("⚙️ Settings")

theme = st.sidebar.radio("🎨 Theme", ["Dark", "Light"])

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.history = ChatMessageHistory()
    st.session_state.messages = []

# --------------------------------------------------
# HISTORY SIDEBAR
# --------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.title("📜 Activity Log")

# Filter and display only user messages (searches)
user_history = [msg['content'] for msg in st.session_state.messages if msg['role'] == 'user']

if user_history:
    for i, query in enumerate(reversed(user_history)):
        st.sidebar.markdown(f"**{len(user_history)-i}.** {query}")
else:
    st.sidebar.caption("No recent activity.")

# --------------------------------------------------
# THEME STYLES
# --------------------------------------------------
# --------------------------------------------------
# THEME STYLES (GLASSMORPHISM & 3D)
# --------------------------------------------------
if theme == "Dark":
    # Dark Mode: Deep Aurora Borealis
    gradient_bg = "linear-gradient(-45deg, #020024, #090979, #00d4ff, #6a11cb)"
    
    # Stronger contrasts for bubbles
    user_bg = "rgba(0, 200, 83, 0.7)"  # High opacity Green
    user_border = "rgba(0, 255, 100, 0.5)"
    
    bot_bg = "rgba(25, 25, 35, 0.9)"   # Higher opacity Dark Gray
    bot_border = "rgba(255, 255, 255, 0.2)"
    
    text_color = "#FFFFFF"             # Pure White
    title_bg = "rgba(0, 0, 0, 0.6)"    # Darker title box
    input_text_color = "#E0E0E0"       # Light grey for input placeholder
else:
    # Light Mode: Soft detailed clouds
    gradient_bg = "linear-gradient(-45deg, #FF9A9E, #FECFEF, #F6D365, #FDA085)"
    
    # Stronger contrasts for bubbles
    user_bg = "rgba(33, 150, 243, 0.8)" # High opacity Blue
    user_border = "rgba(255, 255, 255, 0.5)"
    
    bot_bg = "rgba(255, 255, 255, 0.9)" # Higher opacity White
    bot_border = "rgba(0, 0, 0, 0.1)"
    
    text_color = "#000000"              # Pure Black
    title_bg = "rgba(255, 255, 255, 0.6)"
    input_text_color = "#333333"        # Dark grey for input placeholder

st.markdown(f"""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

body {{
    font-family: 'Poppins', sans-serif !important;
    color: {text_color} !important;
}}

/* Animated Background */
.stApp {{
    background: {gradient_bg};
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
}}

@keyframes gradient {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

/* Chat Container */
.chat-container {{
    display: flex;
    flex-direction: column;
    gap: 15px;
    padding: 20px;
}}

/* Glassmorphism Bubble Base */
.chat-bubble {{
    padding: 15px 25px;
    border-radius: 20px;
    backdrop-filter: blur(15px);         /* Stronger blur */
    -webkit-backdrop-filter: blur(15px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    border: 1px solid;
    max-width: 80%;
    transition: all 0.3s ease;
    transform-style: preserve-3d;
}}

/* 3D Hover Effect */
.chat-bubble:hover {{
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.25);
}}

/* User Bubble Specifics */
.user-bubble {{
    background: {user_bg};
    border-color: {user_border};
    color: white; /* Always white for user bubble usually looks best with strong colors */
    align_self: flex-end;
    margin-left: auto;
    border-bottom-right-radius: 5px;
}}

/* Bot Bubble Specifics */
.bot-bubble {{
    background: {bot_bg};
    border-color: {bot_border};
    color: {text_color};
    align_self: flex-start;
    margin-right: auto;
    border-bottom-left-radius: 5px;
}}

/* Icon Styling */
.icon {{
    font-size: 26px;
    margin-right: 12px;
}}

/* Title Styling - FIXED VISIBILITY */
.title-container {{
    text-align: center;
    padding: 25px;
    margin-bottom: 30px;
    background: {title_bg};       /* Dynamic Background Opacity */
    backdrop-filter: blur(20px);  /* Strong blur "Frosted Acrylic" */
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    border: 1px solid rgba(255,255,255,0.1);
}}

.main-title {{
    font-size: 50px;
    font-weight: 800;
    color: {text_color} !important;
    text-shadow: 2px 2px 0px rgba(0,0,0,0.1); /* Subtle shadow for text pop */
    margin: 0;
}}

/* Input Area Styling */
.stTextInput > div > div > input {{
    background-color: {title_bg};
    color: {input_text_color} !important;
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 12px;
    padding: 10px;
    font-size: 16px;
}}

.stTextInput > div > div > input:focus {{
    border-color: {user_bg};
    box-shadow: 0 0 10px {user_bg};
}}


/* Subtitle Styling */
.subtitle {{
    font-size: 16px;
    color: {text_color} !important;
    opacity: 0.9;
    margin-top: -10px;
    font-weight: 300;
}}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# TITLE
# --------------------------------------------------
st.markdown("""
<div class="title-container">
    <h1 class="main-title">🤖 Syntax Chatbot</h1>
    <p class="subtitle">Experience the future of conversation</p>
</div>
""", unsafe_allow_html=True)



# --------------------------------------------------
# INPUT
# --------------------------------------------------
with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([8, 1])
    with col1:
        user_input = st.text_input("Message", placeholder="💬 Type your message here...", label_visibility="collapsed")
    with col2:
        send = st.form_submit_button("🚀")

if send and user_input.strip():
    st.session_state.history.add_user_message(user_input)

    try:
        response = llm.invoke(
            st.session_state.history.messages
        )
        bot_reply = response.content
        st.session_state.history.add_ai_message(bot_reply)
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "bot", "content": bot_reply})
        
    except Exception as e:
        st.error(f"❌ API Error: {str(e)}")
        if "429" in str(e):
            st.error("⏳ Quota Exceeded (429): You are sending messages too fast. Please wait 15-30 seconds and try again.")
        else:
            st.error("Tip: If you see a 404/503 error, try 'gemini-pro' or check Google AI Studio for status.")

# --------------------------------------------------
# CHAT DISPLAY
# --------------------------------------------------
# Container for chat messages
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="chat-bubble user-bubble">
            <span class="icon">👤</span>
            {msg['content']}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-bubble bot-bubble">
            <span class="icon">🤖</span>
            {msg['content']}
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
