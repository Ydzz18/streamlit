import streamlit as st
from datetime import datetime
import os

chat_db = "chat/chat.txt"

st.title("Welcome sa Chat Group Activity ni Sir")
st.write("Hanap ka kausap mo")

if "username" not in st.session_state:
    st.session_state.username = ""

if "message_sent" not in st.session_state:
    st.session_state.message_sent = False

st.sidebar.header("Settings")
username = st.sidebar.text_input("Enter your name:", value=st.session_state.username, key="user_input")
st.session_state.username = username

def save_message(user, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"{user}|{message}|{timestamp}\n"
    
    os.makedirs(os.path.dirname(chat_db), exist_ok=True)
    
    with open(chat_db, "a", encoding="utf-8") as f:
        f.write(formatted_message)

def load_messages():
    if not os.path.exists(chat_db):
        return []
    
    messages = []
    try:
        with open(chat_db, "r", encoding="utf-8") as f:
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

def clear_chat_history():
    if os.path.exists(chat_db):
        try:
            os.remove(chat_db)
            st.success("Chat history cleared successfully!")
        except Exception as e:
            st.error(f"Error clearing chat history: {e}")
    else:
        st.info("No chat history to clear.")

st.markdown("### Chat Messages")
st.subheader("Messages")
messages = load_messages()

# Display all messages with bubble style
if messages:
    for msg in messages:
        # Check if message is from current user
        is_current_user = msg['user'] == st.session_state.username
        
        if is_current_user:
            # Current user - right aligned with different color
            bubble_html = f"""
            <div style="margin-bottom: 15px; display: flex; justify-content: flex-end;">
                <div style="
                    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    color: white;
                    padding: 12px 16px;
                    border-radius: 15px;
                    max-width: 70%;
                    word-wrap: break-word;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                ">
                    <div style="font-weight: bold; margin-bottom: 5px; font-size: 0.9em;">
                        {msg['user']}
                    </div>
                    <div style="margin-bottom: 8px; font-size: 0.95em;">
                        {msg['message']}
                    </div>
                    <div style="font-size: 0.75em; opacity: 0.8; text-align: right;">
                        {msg['timestamp']}
                    </div>
                </div>
            </div>
            """
        else:
            # Other users - left aligned with original color
            bubble_html = f"""
            <div style="margin-bottom: 15px; display: flex; justify-content: flex-start;">
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 12px 16px;
                    border-radius: 15px;
                    max-width: 70%;
                    word-wrap: break-word;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                ">
                    <div style="font-weight: bold; margin-bottom: 5px; font-size: 0.9em;">
                        {msg['user']}
                    </div>
                    <div style="margin-bottom: 8px; font-size: 0.95em;">
                        {msg['message']}
                    </div>
                    <div style="font-size: 0.75em; opacity: 0.8;">
                        {msg['timestamp']}
                    </div>
                </div>
            </div>
            """
        
        st.markdown(bubble_html, unsafe_allow_html=True)
else:
    st.info("No messages yet. Start the conversation!")

st.markdown("---")
st.subheader("Send a Message")

def send_message_callback():
    """Callback function to handle message sending"""
    message = st.session_state.message_input.strip()
    
    if not st.session_state.username:
        st.warning("Please enter your name in the sidebar before sending a message.")
    elif not message:
        st.warning("Please enter a message before sending.")
    else:
        save_message(st.session_state.username, message)
        st.session_state.message_sent = True
        st.session_state.message_input = ""  # Clear the input

col1, col2 = st.columns([4, 1])
with col1:
    send_message = st.text_input("Your message:", placeholder="Type your message here...", key="message_input")
    
with col2:
    st.write("")
    submit_btn = st.button("Send", use_container_width=True, type="primary", on_click=send_message_callback)

# Show success message if message was just sent
if st.session_state.message_sent:
    st.success("✅ Message sent!")
    st.session_state.message_sent = False
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("Options")

if st.sidebar.button("Refresh Chat", use_container_width=True):
    st.rerun()

if st.sidebar.button("Clear Chat History", use_container_width=True):
    clear_chat_history()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("Stats")
st.sidebar.metric("Messages Sent", len(messages))


users = set(msg["user"] for msg in messages)
st.sidebar.metric("Unique Users", len(users))

if users:
    st.sidebar.write("**Users in Chat:**")
    for user in sorted(users):
        st.sidebar.write(f"- {user}")  