# import os
# import json
# import re
# from datetime import datetime
# from dotenv import load_dotenv
# from collections import defaultdict
# from pydantic import BaseModel, Field
# from langchain.tools import Tool
# from config import llm

# # Initialize user routine memory
# user_routine_memory = defaultdict(lambda: {
#     "last_concern": None,
#     "activities": {},
#     "created_at": datetime.now()
# })

# # Pydantic models for tool requests
# class ConcernCategorizeRequest(BaseModel):
#     user_message: str = Field(description="Message from the user to be categorized")

# class UserRoutineRequest(BaseModel):
#     user_id: str = Field(description="Unique identifier for the user")
#     user_message: str = Field(description="Message from the user to process")

# class SuggestMealPlan(BaseModel):
#     user_id: str = Field(description="Unique identifier for the user")
#     meal_type: str = Field(description="Type of meal to suggest (e.g., breakfast, lunch, dinner)")
#     dietary_preferences: str = Field(description="User's dietary preferences or restrictions i.e., vegetarian, gluten-free, mid-income, budget-friendly meal etc.")

# def categorize_concern(user_message: str):
#     """
#     Categorizes user messages as 'routine-related', 'life-event-related', or 'neutral-chat'.
#     """
#     prompt = f"""
#     Analyze the following user statement and categorize it as:
#     - 'routine-related' if it involves sleep, diet, exercise, or structured activities.
#     - 'life-event-related' if it is about relationships, emotions, or personal experiences.
#     - 'neutral-chat' if it is casual conversation without concerns.

#     User statement: "{user_message}"

#     Respond ONLY with one of these categories: 'routine-related', 'life-event-related', or 'neutral-chat'.
#     DO NOT include any extra explanation.
#     """
    
#     response = llm.invoke(prompt)
#     response_text = response.content if hasattr(response, "content") else str(response)

#     match = re.search(r"(routine-related|life-event-related|neutral-chat)", response_text, re.IGNORECASE)
#     return match.group(1).lower().strip() if match else "neutral-chat"

# def talk_with_user(user_id: str, user_message: str):
#     """
#     Tracks user-specific routine details and provides suggestions dynamically.
#     """
#     concern_type = categorize_concern(user_message)

#     if concern_type == "routine-related":
#         # Step 1: Figure out what activity the user is talking about
#         activity_prompt = f"""Extract the main routine-related activity from this message:
#         "{user_message}"
#         """
#         activity_response = llm.invoke(activity_prompt)
#         activity = activity_response.content.strip() if hasattr(activity_response, "content") else str(activity_response).strip()

#         # Step 2: Store the message in the right place
#         if activity not in user_routine_memory[user_id]["activities"]:
#             user_routine_memory[user_id]["activities"][activity] = []

#         # Step 3: Get a personalized suggestion
#         user_routine_memory[user_id]["activities"][activity].append({
#             "message": user_message,
#             "timestamp": datetime.now()
#         })

#         user_routine_memory[user_id]["last_concern"] = activity

#         suggestion_prompt = f"""
#         Generate a brief, ADHD-friendly suggestion for this routine activity: {activity}
        
#         Guidelines:
#         - Keep it under 2 sentences
#         - Make it specific and actionable
#         - Include a time-based element if relevant
#         - Use positive reinforcement
#         - Consider ADHD challenges
        
#         Respond with ONLY the suggestion, no extra text.
#         """
#         suggestion_response = llm.invoke(suggestion_prompt)
#         suggestion_text = suggestion_response.content if hasattr(suggestion_response, "content") else str(suggestion_response)

#         return f"Noted your {activity} routine. {suggestion_text}"

#     elif concern_type == "life-event-related" or concern_type == "neutral-chat":
#         user_routine_memory[user_id]["last_concern"] = concern_type

#         suggestion_prompt = f"""
#         You are a helpful assistant that responds to user messages in a way that is appropriate for the type of concern: {concern_type}
        
#         - For life-event-related concerns, provide a supportive and empathetic response.
#         - For neutral-chat concerns, engage in a friendly conversation.
#         - Be concise to user questions and don't be too verbose.

#         User message: "{user_message}"
#         """
#         response = llm.invoke(suggestion_prompt)
#         response_text = response.content if hasattr(response, "content") else str(response)

#         return response_text

#     return "I'm listening! Feel free to share more."

# def meal_plan_suggestion(user_id: str, meal_type: str, dietary_preferences: str):
#     """
#     Suggests a meal plan based on user preferences.
#     """
#     meal_prompt = f"""
#     Suggest a {meal_type} meal plan for a user with the following dietary preferences: {dietary_preferences}.
    
#     Guidelines:
#     - Include 3 meal options
#     - Ensure the meals are budget-friendly and easy to prepare
#     - Provide a brief description of each meal
#     """
    
#     response = llm.invoke(meal_prompt)
#     response_text = response.content if hasattr(response, "content") else str(response)

#     return response_text


# # Tool definitions for use with LLM frameworks
# concern_categorize_tool = {
#     "type": "function",
#     "function": {
#         "name": "categorize_concern",
#         "description": "Categorizes a user message by concern type",
#         "parameters": ConcernCategorizeRequest.model_json_schema(),
#     },
# }

# user_routine_tool = {
#     "type": "function",
#     "function": {
#         "name": "talk_with_user",
#         "description": "Processes user messages and provides ADHD-friendly responses",
#         "parameters": UserRoutineRequest.model_json_schema(),
#     },
# }

# meal_plan_suggestion_tool = {
#     "type": "function",
#     "function": {
#         "name": "meal_plan_suggestion",
#         "description": "Suggests a meal plan based on user preferences",
#         "parameters": SuggestMealPlan.model_json_schema(),
#     },
# }

# # For compatibility with your existing code
# categorize_concern_tool = Tool(
#     name="categorize_concern",
#     description="Categorizes a user message as 'routine-related', 'life-event-related', or 'neutral-chat'.",
#     func=categorize_concern
# )

# track_user_routine_tool = Tool(
#     name="track_user_routine",
#     description="Tracks a user's routine and provides personalized suggestions according to the concern type.",
#     func=talk_with_user
# )

# meal_plan_suggestion_tool = Tool(
#     name="meal_plan_suggestion",
#     description="Suggests a meal plan based on user preferences.",
#     func=meal_plan_suggestion
# )


# # Collection of tools
# adhd_assistant_tools = [
#     concern_categorize_tool,
#     user_routine_tool,
#     meal_plan_suggestion_tool,
# ]

# # Original tools list for backward compatibility
# TOOLS = [categorize_concern_tool, track_user_routine_tool, meal_plan_suggestion_tool]

from langchain.tools import Tool
from datetime import datetime
from collections import defaultdict
import re
import json
from config import llm

# Memory
user_routine_memory = defaultdict(lambda: {
    "last_concern": None,
    "activities": {},
    "created_at": datetime.now()
})

def categorize_concern(user_message: str):
    """Categorize user messages as 'routine-related', 'life-event-related', or 'neutral-chat'."""
    prompt = f"""
    Analyze this and categorize it as 'routine-related', 'life-event-related', or 'neutral-chat'.
    Statement: "{user_message}"
    Only respond with the category.
    """
    response = llm.invoke(prompt)
    match = re.search(r"(routine-related|life-event-related|neutral-chat)", response.content, re.IGNORECASE)
    return match.group(1).lower().strip() if match else "neutral-chat"

def talk_with_user(user_id: str, user_message: str):
    """Process user messages and provide appropriate responses."""
    concern_type = categorize_concern(user_message)

    if concern_type == "routine-related":
        activity_prompt = f"Extract the main routine activity from: {user_message}"
        activity_response = llm.invoke(activity_prompt)
        activity = activity_response.content.strip()

        if activity not in user_routine_memory[user_id]["activities"]:
            user_routine_memory[user_id]["activities"][activity] = []

        user_routine_memory[user_id]["activities"][activity].append({
            "message": user_message,
            "timestamp": datetime.now()
        })
        user_routine_memory[user_id]["last_concern"] = activity

        suggestion_prompt = f"""
        Generate an ADHD-friendly tip for: {activity}
        - Short
        - Actionable
        - Use reinforcement
        """
        suggestion_response = llm.invoke(suggestion_prompt)
        return f"Noted your {activity} routine. {suggestion_response.content}"

    else:
        user_routine_memory[user_id]["last_concern"] = concern_type
        empathy_prompt = f"""User message: "{user_message}". Provide a short, appropriate response for: {concern_type}"""
        return llm.invoke(empathy_prompt).content

def meal_plan_suggestion(user_id: str, user_message: str):
    """Suggest meal plans based on user preferences."""
    # Step 1: Ask the LLM to extract intent/fields from natural language
    extraction_prompt = f"""
    You are helping extract structured meal preferences from user input.
    Extract the following fields from the message below:
    - Meal Type (breakfast, lunch, dinner)
    - Dietary Preferences (e.g., vegetarian, halal, gluten-free, budget-friendly)

    Respond in JSON format like:
    {{
        "meal_type": "...",
        "dietary_preferences": "..."
    }}

    User message: "{user_message}"
    """
    extraction_response = llm.invoke(extraction_prompt)
    extraction_text = extraction_response.content

    try:
        parsed = json.loads(extraction_text)
        meal_type = parsed.get("meal_type", "any")
        dietary_preferences = parsed.get("dietary_preferences", "none")
    except json.JSONDecodeError:
        return "Sorry, I couldn't understand your preferences. Could you rephrase?"

    # Step 2: Generate meal plan using extracted preferences
    meal_prompt = f"""
    Suggest a {meal_type} meal for dietary preference: {dietary_preferences}.
    - Include 3 simple, budget-friendly options
    - Use short descriptions
    """
    response = llm.invoke(meal_prompt)
    return response.content

# Define tools for the agent framework
talk_tool = Tool(
    name="talk_with_user",
    description="Process user messages and provide appropriate responses based on the type of concern.",
    func=talk_with_user
)

meal_tool = Tool(
    name="meal_plan_suggestion",
    description="Suggest meal plans based on user preferences and dietary restrictions.",
    func=meal_plan_suggestion
)

# List of tools for the agent
TOOLS = [talk_tool, meal_tool]