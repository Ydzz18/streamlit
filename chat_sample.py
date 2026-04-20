import streamlit as st
from datetime import datetime
import os

# File path for chat database
CHAT_DB_PATH = "chat/chat.txt"

st.set_page_config(page_title="Group Chat", layout="wide")
st.title("💬 Group Chat Application")
st.write("Welcome to the group chat! Share messages with everyone.")

# Initialize session state
if "username" not in st.session_state:
    st.session_state.username = ""

# Sidebar for user settings
st.sidebar.header("⚙️ Settings")
username = st.sidebar.text_input("Enter your name:", value=st.session_state.username, key="user_input")
st.session_state.username = username

# Function to save message to chat.txt
def save_message(user, message):
    """Save a message to the chat database."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"{user}|{message}|{timestamp}\n"
    
    # Ensure chat directory exists
    os.makedirs(os.path.dirname(CHAT_DB_PATH), exist_ok=True)
    
    # Append message to chat.txt
    with open(CHAT_DB_PATH, "a", encoding="utf-8") as f:
        f.write(formatted_message)

# Function to load all messages from chat.txt
def load_messages():
    """Load all messages from the chat database."""
    if not os.path.exists(CHAT_DB_PATH):
        return []
    
    messages = []
    try:
        with open(CHAT_DB_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split("|")
                    if len(parts) == 3:
                        user, message, timestamp = parts
                        messages.append({
                            "user": user,
                            "message": message,
                            "timestamp": timestamp
                        })
    except Exception as e:
        st.error(f"Error loading messages: {e}")
    
    return messages

# Function to clear all messages
def clear_chat_history():
    """Clear all messages from the chat database."""
    if os.path.exists(CHAT_DB_PATH):
        os.remove(CHAT_DB_PATH)
        st.success("Chat history cleared!")

# Display chat area
st.markdown("---")
st.subheader("📝 Chat Messages")

# Load and display messages
messages = load_messages()

if messages:
    for msg in messages:
        with st.container():
            col1, col2 = st.columns([1, 5])
            with col1:
                st.caption(f"**{msg['user']}**")
                st.caption(f"_{msg['timestamp']}_")
            with col2:
                st.write(msg['message'])
            st.divider()
else:
    st.info("No messages yet. Start the conversation!")

# Message input area
st.markdown("---")
st.subheader("✍️ Send a Message")

col1, col2 = st.columns([4, 1])

with col1:
    message_input = st.text_area("Your message:", placeholder="Type your message here...")

with col2:
    st.write("")  # Add spacing
    send_button = st.button("Send", use_container_width=True, type="primary")

# Handle sending message
if send_button:
    if not st.session_state.username.strip():
        st.error("⚠️ Please enter your name in the sidebar!")
    elif not message_input.strip():
        st.warning("⚠️ Please enter a message!")
    else:
        # Save message to database
        save_message(st.session_state.username, message_input)
        st.success("✅ Message sent!")
        st.rerun()

# Sidebar options
st.sidebar.markdown("---")
st.sidebar.subheader("Options")

if st.sidebar.button("🔄 Refresh Chat", use_container_width=True):
    st.rerun()

if st.sidebar.button("🗑️ Clear Chat History", use_container_width=True):
    clear_chat_history()
    st.rerun()

# Display chat stats
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Statistics")
st.sidebar.metric("Total Messages", len(messages))

# Display active users
active_users = set(msg["user"] for msg in messages)
st.sidebar.metric("Active Users", len(active_users))

if active_users:
    st.sidebar.write("**Users:**")
    for user in sorted(active_users):
        st.sidebar.write(f"• {user}")
