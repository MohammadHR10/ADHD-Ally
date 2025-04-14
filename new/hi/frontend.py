import streamlit as st
import requests
import json

# The URL of your Flask backend API (make sure it matches the Flask server)
BACKEND_URL = "http://localhost:5001/chat"  # Replace with the correct URL if hosted remotely

def send_message(user_id: str, message: str):
    """Send the user's message to the backend and get the response."""
    try:
        # Prepare the data to be sent in the POST request
        data = {
            "user_id": user_id,
            "message": message
        }

        # Send the POST request to the backend
        response = requests.post(BACKEND_URL, json=data)

        # Check if the response is valid
        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            error_message = response.json().get("error", "Something went wrong.")
            return f"Error: {error_message}"

    except requests.exceptions.RequestException as e:
        # If the request fails, show an error message
        return f"Connection error: {str(e)}"

def main():
    """Streamlit frontend for the ADHD assistant."""
    st.title("🧠 ADHD AI Assistant")
    
    # Display a text input for the user to type their message
    user_message = st.text_input("You:", "")

    if user_message:
        user_id = "default_user"  # In a real application, you'd have proper user management
        # Send the message to the backend and get the response
        response = send_message(user_id, user_message)
        
        # Display the AI response
        st.write(f"🧠 AI: {response}")

if __name__ == "__main__":
    main()