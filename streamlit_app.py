import streamlit as st
import requests

# Backend endpoint (adjust host/port if needed)
BACKEND_URL = "http://localhost:8000/chat/chat"

st.set_page_config(page_title="Agentic Hotel Assistant", page_icon="🏨", layout="centered")

st.title("Agentic Hotel Assistant")

# --- Custom CSS for elegant chat bubbles & scrollable chat box ---
st.markdown("""
    <style>
    body {
        background-color: #fafafa;
    }
    .chat-box {
        height: 500px;      /* adjust height as needed */
        overflow-y: auto;
        padding: 15px;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        background-color: #1E1E1E;
    }
    .chat-bubble {
        padding: 12px 18px;
        border-radius: 18px;
        margin: 8px;
        max-width: 75%;
        font-size: 15px;
        line-height: 1.4;
        word-wrap: break-word;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .user-bubble {
        background-color: #1877F2;         
        color: white;
        margin-left: auto;
        text-align: right;
    }
    .assistant-bubble {
        background-color: #2A2F32;
        color: #ffffff;
        margin-right: auto;
        text-align: left;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = "1"   # default thread ID = "1"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Sidebar controls
st.sidebar.title("⚙️ Controls")

# Editable thread ID
thread_input = st.sidebar.text_input("Thread ID", st.session_state["thread_id"])
if thread_input.strip():
    st.session_state["thread_id"] = thread_input.strip()

if st.sidebar.button("🧹 Clear Chat"):
    st.session_state["messages"] = []

if st.sidebar.button("🆕 New Conversation (keep ID)"):
    st.session_state["messages"] = []

st.sidebar.markdown(f"**Active Thread ID:** `{st.session_state['thread_id']}`")

# Chat display inside scrollable container
chat_html = "<div class='chat-box'>"
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        chat_html += f"<div class='chat-bubble user-bubble'>{msg['content']}</div>"
    else:
        chat_html += f"<div class='chat-bubble assistant-bubble'>{msg['content']}</div>"
chat_html += "</div>"

st.markdown(chat_html, unsafe_allow_html=True)

# Chat input box
if prompt := st.chat_input("Ask me anything about your hotel booking..."):
    # Add user message
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # Send request to backend
    try:
        payload = {
            "thread_id": st.session_state["thread_id"],
            "user_message": prompt
        }
        response = requests.post(BACKEND_URL, json=payload)
        if response.status_code == 200:
            bot_reply = response.json().get("reply", "⚠️ No reply received.")
        else:
            bot_reply = f"⚠️ Error {response.status_code}: Could not connect."
    except Exception as e:
        bot_reply = f"⚠️ Exception: {str(e)}"

    # Add assistant response
    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})

    # Force rerun to refresh chat box display
    st.rerun()
