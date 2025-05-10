import streamlit as st
import requests
import cv2
import numpy as np
from speech_emotion import speech_emotion
from audio import speech_recognition
import time
import pandas as pd

BACKEND_URL = "http://localhost:5001/chat"

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = "user_" + str(int(time.time()))
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'emotion_history' not in st.session_state:
    st.session_state.emotion_history = []
if 'is_listening' not in st.session_state:
    st.session_state.is_listening = False
if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False

def process_video():
    """Process video feed and detect emotions"""
    cap = cv2.VideoCapture(0)
    while st.session_state.is_listening:
        ret, frame = cap.read()
        if not ret:
            continue
            
        try:
            # Convert to RGB for Streamlit
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Get emotion from frame
            emotion = speech_emotion.get_emotion_summary(st.session_state.user_id)
            
            # Add emotion to history
            st.session_state.emotion_history.append({
                'emotion': emotion['dominant_emotion'],
                'confidence': emotion['confidence'],
                'timestamp': time.time()
            })
            
            # Display frame
            st.image(frame_rgb, caption=f"Current Emotion: {emotion['dominant_emotion']} ({emotion['confidence']:.0%})")
            
        except Exception as e:
            st.error(f"Error processing video: {str(e)}")
            continue
            
        time.sleep(0.1)
    
    cap.release()

def main():
    st.title("🧠 ADHD AI Assistant with Emotion & Speech Recognition")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("Controls")
        
        # Emotion recognition controls
        st.subheader("Emotion Recognition")
        if st.button("Start/Stop Emotion Recognition"):
            st.session_state.is_listening = not st.session_state.is_listening
            if st.session_state.is_listening:
                speech_emotion.start_listening(st.session_state.user_id)
            else:
                speech_emotion.stop_listening()
        
        # Speech recognition controls
        st.subheader("Speech Recognition")
        if st.button("Start/Stop Speech Recording"):
            st.session_state.is_recording = not st.session_state.is_recording
            if st.session_state.is_recording:
                speech_recognition.start_recording()
            else:
                speech_recognition.stop_recording()
                # Process the recorded audio
                transcribed_text = speech_recognition.process_audio()
                if transcribed_text:
                    st.session_state.last_transcription = transcribed_text
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Video Feed")
        if st.session_state.is_listening:
            process_video()
        else:
            st.info("Click 'Start/Stop Emotion Recognition' to begin")
    
    with col2:
        st.header("Chat")
        
        # Display transcribed text if available
        if 'last_transcription' in st.session_state:
            st.text_area("Transcribed Speech:", st.session_state.last_transcription, height=100)
        
        # Chat input
        user_message = st.text_input("You:", "")
        if user_message:
            # Get current emotion state
            emotion_state = speech_emotion.get_emotion_summary(st.session_state.user_id)
            
            # Send message to backend with emotion context
            response = requests.post(BACKEND_URL, json={
                "user_id": st.session_state.user_id,
                "message": user_message,
                "emotion": emotion_state['dominant_emotion'],
                "emotion_confidence": emotion_state['confidence']
            })

            if response.status_code == 200:
                response_text = response.json()['response']
                # Add to chat history
                st.session_state.chat_history.append({
                    'user': user_message,
                    'assistant': response_text,
                    'emotion': emotion_state['dominant_emotion'],
                    'timestamp': time.time()
                })
                st.markdown(f"**🧠 AI:** {response_text}")
            else:
                st.error(response.json().get("error", "Something went wrong."))
        
        # Display chat history
        st.header("Chat History")
        for chat in st.session_state.chat_history:
            st.write(f"👤 You: {chat['user']}")
            st.write(f"🤖 Assistant: {chat['assistant']}")
            if 'emotion' in chat:
                st.write(f"😊 Emotion: {chat['emotion']}")
            st.write("---")
    
    # Emotion history
    st.header("Emotion History")
    if st.session_state.emotion_history:
        emotion_df = pd.DataFrame(st.session_state.emotion_history)
        st.line_chart(emotion_df['confidence'])

if __name__ == "__main__":
    main()
