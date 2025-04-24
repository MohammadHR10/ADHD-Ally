import streamlit as st
import requests

BACKEND_URL = "http://localhost:5001/chat"

st.title("🧠 ADHD AI Assistant")
user_message = st.text_input("You:", "")

if user_message:
    response = requests.post(BACKEND_URL, json={
        "user_id": "default_user",
        "message": user_message
    })

    if response.status_code == 200:
        st.markdown(f"**🧠 AI:** {response.json()['response']}")
    else:
        st.error(response.json().get("error", "Something went wrong."))
