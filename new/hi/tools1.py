from langchain.tools import Tool
from datetime import datetime
from collections import defaultdict
import re
from config import llm, memory


def categorize_concern(user_message: str):
    prompt = f"""
    Analyze this and categorize it as 'routine-related', 'life-event-related', or 'neutral-chat'.
    Statement: "{user_message}"
    Only respond with the category.
    """
    response = llm.invoke(prompt)
    match = re.search(r"(routine-related|life-event-related|neutral-chat)", response.content, re.IGNORECASE)
    return match.group(1).lower().strip() if match else "neutral-chat"

def talk_with_user(input_text: str):
    match = re.search(r"User ID: (.+?)\. User input: (.+)", input_text)
    user_id = match.group(1).strip() if match else "default_user"
    user_message = match.group(2).strip() if match else input_text

    concern_type = categorize_concern(user_message)

    if concern_type == "routine-related":
        activity_prompt = f"Extract the main routine activity from: {user_message}"
        activity_response = llm.invoke(activity_prompt)
        activity = activity_response.content.strip()

        memory.save_context(
            {"input": user_message},
            {"output": f"[ROUTINE] {activity} | Logged at {datetime.now().isoformat()}"}
        )

        suggestion_prompt = f"""
        Generate an ADHD-friendly tip for: {activity}
        - Short
        - Actionable
        - Use reinforcement
        """
        suggestion_response = llm.invoke(suggestion_prompt)
        return f"Noted your {activity} routine. {suggestion_response.content}"

    else:
        memory.save_context(
            {"input": user_message},
            {"output": f"[CONCERN] {concern_type} | Logged at {datetime.now().isoformat()}"}
        )
        empathy_prompt = f"""User message: "{user_message}". Provide a short, appropriate response for: {concern_type}"""
        return llm.invoke(empathy_prompt).content

from datetime import datetime

def meal_plan_suggestion(input_text: str):
    # Step 1: Parse meal type + dietary preference
    if "User ID" not in input_text:
        extract_prompt = f"""
        From the following request, extract:
        - Meal Type (e.g., breakfast, lunch, dinner)
        - Dietary Preference (e.g., vegetarian, low-carb, no preference)

        Request: "{input_text}"

        Format your response as:
        Meal Type: ...
        Dietary: ...
        """
        parsed = llm.invoke(extract_prompt).content
        match = re.search(r"Meal Type: (.+?)\nDietary: (.+)", parsed)
        if not match:
            return "❌ Could not understand your request. Try: 'I want a vegetarian lunch.'"

        meal_type = match.group(1).strip()
        dietary_preferences = match.group(2).strip()
        user_id = "default_user"
    else:
        match = re.search(r"User ID: (.+?)\. Meal Type: (.+?)\. Dietary: (.+)", input_text)
        if not match:
            return (
                "❌ Input format is incorrect. Please use: "
                "'User ID: [user_id]. Meal Type: [meal_type]. Dietary: [dietary_preferences]'."
            )
        user_id = match.group(1).strip()
        meal_type = match.group(2).strip()
        dietary_preferences = match.group(3).strip()

    # Step 2: Get meal plan
    meal_prompt = f"""
    Suggest a {meal_type} meal for dietary preference: {dietary_preferences}.
    - 3 simple options
    - Budget-friendly
    - Short descriptions
    """
    response_text = llm.invoke(meal_prompt).content.strip()

    # Step 3: Save to memory
    memory.save_context(
        {"input": input_text},
        {"output": f"[MEAL_PLAN] {response_text} | Meal Type: {meal_type}, Dietary: {dietary_preferences}, User: {user_id}, Time: {datetime.now().isoformat()}"}
    )

    # Step 4: Return to user
    return response_text

# Tools list
TOOLS = [
    Tool(name="track_user_routine", func=talk_with_user, description="Track routines from user input"),
    Tool(name="meal_plan_suggestion", func=meal_plan_suggestion, description="Suggests a meal plan based on type and dietary preference. Use for ANY food-related requests, even shoeter queries. Think as if you are a chef or a food expert and know all about food. So suggest likewise.")
]