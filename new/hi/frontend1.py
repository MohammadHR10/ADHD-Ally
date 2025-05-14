import streamlit as st
from audio import speech_recognition  # Ensure you have: speech_recognition = SpeechRecognition() in audio.py
import requests
import time

BACKEND_URL = "http://localhost:5001/chat"

# Session setup
if 'user_id' not in st.session_state:
    st.session_state.user_id = f"user_{int(time.time())}"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.title("🧠 ADHD Routine Assistant")

st.markdown("Choose how you want to interact:")

# Choose Input Mode
mode = st.radio("Input Mode", ["Type", "Speak"], horizontal=True)

# Get Input
user_message = ""
if mode == "Type":
    user_message = st.text_input("📝 Enter your message:")
elif mode == "Speak":
    if st.button("🎤 Record Now"):
        try:
            user_message = speech_recognition.record_and_transcribe()
            st.success(f"You said: {user_message}")
        except Exception as e:
            st.error(f"Speech error: {e}")

# Submit to backend
if user_message:
    with st.spinner("Thinking..."):
        try:
            response = requests.post(BACKEND_URL, json={
                "user_id": st.session_state.user_id,
                "message": user_message
            })

            if response.status_code == 200:
                reply = response.json()["response"]
                st.session_state.chat_history.append(("You", user_message))
                st.session_state.chat_history.append(("AI", reply))
                st.success(reply)
            else:
                st.error("Backend error: " + response.text)
        except Exception as e:
            st.error(f"Request failed: {e}")

# Show chat history
st.header("🗂️ Chat History")
for sender, msg in st.session_state.chat_history[::-1]:  # Show latest first
    st.markdown(f"**{sender}:** {msg}")
