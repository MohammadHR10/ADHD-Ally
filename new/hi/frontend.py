import streamlit as st
import requests

BACKEND_URL = "http://localhost:5001/chat"

def send_message(user_id: str, message: str):
    try:
        data = {"user_id": user_id, "message": message}
        response = requests.post(BACKEND_URL, json=data)
        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            return f"Error: {response.json().get('error', 'Something went wrong.')}"
    except requests.exceptions.RequestException as e:
        return f"Connection error: {str(e)}"

def main():
    st.title("🧠 ADHD AI Assistant")
    user_message = st.text_input("You:", key="input")

    if user_message:
        user_id = "default_user"  # You can add session-based ID later
        response = send_message(user_id, user_message)
        st.markdown(f"**🧠 AI:** {response}")

if __name__ == "__main__":
    main()
