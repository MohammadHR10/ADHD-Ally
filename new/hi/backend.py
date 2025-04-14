from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv
from tools import talk_with_user

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize Flask app
app = Flask(__name__)

# Allow CORS for your Streamlit app's specific origin (replace with the correct URL if needed)
CORS(app, resources={r"/chat": {"origins": "http://localhost:8501"}})  # Replace with your Streamlit URL

@app.route("/chat", methods=["POST"])
def chat():
    """Handles incoming messages and sends a response back."""
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Validate if the necessary data is present
        if not data or "user_id" not in data or "message" not in data:
            return jsonify({"error": "Both 'user_id' and 'message' are required"}), 400

        user_id = data.get("user_id", "default_user")
        message = data.get("message", "")

        # Check if the message is empty
        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # Process the message and get the response
        response = talk_with_user(user_id, message)

        # Return the response
        return jsonify({"response": response})

    except Exception as e:
        # Log the error for debugging
        print(f"Error: {str(e)}")
        
        # Return a 500 Internal Server Error with error details
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)