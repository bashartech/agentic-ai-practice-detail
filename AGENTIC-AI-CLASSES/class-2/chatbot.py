# import chainlit as cl
# from main import agent, configure
# from agents import Runner
# import asyncio
# session_histories = {}

# @cl.on_message
# async def main(message: cl.Message):
#     user_id = message.author  # it gives a unique ID for each user or session


# # If it’s the user’s first message, we create an empty list to start storing their messages.

#     if user_id not in session_histories:
#         session_histories[user_id] = []

#     history = session_histories[user_id]
#     context = "\n".join([f"{item['role']}: {item['content']}" for item in history])
#     context += f"\nuser: {message.content}"

# # This adds the latest user input to their history list.
#     session_histories[user_id].append({"role": "user", "content": message.content})

#     await cl.Message(
#         content=f"Thinking..",
#     ).send()

#     result = await Runner.run(
#         agent, context
#     )
#     ai_result = result.final_output

#     session_histories[user_id].append({"role": "assistant", "content": ai_result})

#     # Send a response back to the user
#     await cl.Message(
#         content=f"AI Response {ai_result}",
#     ).send()
import chainlit as cl
from main import agent, configure
from agents import Runner


# Store session histories
session_histories = {}

@cl.on_chat_start
async def start():
    """Initialize the chat session"""
    await cl.Message(
        content="🤖 **Smart AI Assistant** is ready!\n\nI can help you with:\n📧 **Send emails** - Just tell me who to email and what message\n🌤️ **Get weather** - Ask about weather in any city\n💱 **Currency rates** - Get exchange rates\n🧮 **General questions** - Ask me anything!\n\n**Example:** *'Send an email to john@example.com saying the meeting is at 3pm'*"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages"""
    
    # Handle special commands first
    if message.content.lower() == "/clear":
        user_id = cl.user_session.get("id", "default")
        if user_id in session_histories:
            session_histories[user_id] = []
        await cl.Message(content="🗑️ Chat history cleared!").send()
        return
    
    # Get user session ID
    user_id = cl.user_session.get("id", "default")
    
    # Initialize session history if not exists
    if user_id not in session_histories:
        session_histories[user_id] = []
    
    # Add user message to history
    session_histories[user_id].append({
        "role": "user", 
        "content": message.content
    })
    
    # Show thinking message
    thinking_msg = await cl.Message(content="🤔 Thinking...").send()
    
    try:
        print(f"🔄 Processing message: {message.content}")
        
        # Run the agent with the current message
        result = await Runner.run(
            agent,
            input=message.content,
            run_config=configure,
            max_turns=10
        )
        
        print(f"✅ Agent result: {result.final_output}")
        
        ai_response = result.final_output
        
        # Add AI response to history
        session_histories[user_id].append({
            "role": "assistant", 
            "content": ai_response
        })
        
        # Update the thinking message with the result
        thinking_msg.content = f"🤖 {ai_response}"
        await thinking_msg.update()
        
    except Exception as e:
        error_msg = f"❌ Sorry, I encountered an error: {str(e)}"
        await thinking_msg.update(content=error_msg)
        print(f"❌ Error in agent: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    cl.run()
