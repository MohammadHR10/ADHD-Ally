# import os
# from langchain.memory import ConversationBufferMemory
# from langchain.agents import initialize_agent, AgentType
# from config import llm
# from tools import TOOLS# Import the talk_with_user function directly

# # Initialize memory
# # Even though there's a deprecation warning, we'll keep using it as you need this functionality
# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# # Initialize the agent
# # We'll keep using this despite the deprecation warning since you need the functionality
# agent = initialize_agent(
#     tools=TOOLS,
#     llm=llm,
#     agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
#     memory=memory,
#     verbose=True
# )

# def main():
#     """Main entry point for the ADHD assistant."""
#     print("🧠 ADHD AI Assistant: Hello! I'm here to help you manage your tasks and daily life.")
#     print("Type 'exit' to end the conversation.")
    
#     user_id = "default_user"  # In a real application, you'd have proper user management
    
#     while True:
#         try:
#             user_input = input("\nYou: ").strip()
            
#             if user_input.lower() in ['exit', 'quit', 'bye']:
#                 print("\n🧠 AI: Take care! Remember to break down tasks into small steps. You've got this! 💪")
#                 break
            
#             if not user_input:
#                 continue
            
#             # Use the agent's run method with just the user input
#             response = agent.run(user_input)
            
#             # Also save to agent memory for historical context
#             memory.save_context(
#                 {"input": user_input},
#                 {"output": response}
#             )
            
#             # Print the response with emoji
#             print(f"\n🧠 AI: {response}")
            
#         except KeyboardInterrupt:
#             print("\n\n🧠 AI: Goodbye! Stay focused and take it one step at a time! 🌟")
#             break
#         except Exception as e:
#             print(f"\n🧠 AI: I apologize, but I encountered an error: {str(e)}")
#             print("Please check your API key and try again.")

# if __name__ == "__main__":
#     main()

import os
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from config import llm
from tools import TOOLS  # tools from Option 1 (manual input parsing)

# Memory (will show a deprecation warning, but still functional)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Agent initialized with legacy ReAct type
agent = initialize_agent(
    tools=TOOLS,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

def main():
    print("🧠 ADHD AI Assistant: Hello! I'm here to help you manage your tasks and daily life.")
    print("Type 'exit' to end the conversation.")
    
    user_id = "default_user"

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\n🧠 AI: Take care! Remember to break down tasks into small steps. You've got this! 💪")
                break

            if not user_input:
                continue

            # Pack user_id and input into a single string
            context_string = f"User ID: {user_id}. User input: {user_input}"
            response = agent.run(context_string)

            memory.save_context({"input": user_input}, {"output": response})
            print(f"\n🧠 AI: {response}")

        except KeyboardInterrupt:
            print("\n\n🧠 AI: Goodbye! Stay focused and take it one step at a time! 🌟")
            break
        except Exception as e:
            print(f"\n🧠 AI: I apologize, but I encountered an error: {str(e)}")

if __name__ == "__main__":
    main()