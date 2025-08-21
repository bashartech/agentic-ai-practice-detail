from agents import Runner, SQLiteSession
from agentz.agents_tutor import personal_assistant
import asyncio
from openai.types.responses import ResponseTextDeltaEvent

async def main():
  
  session = SQLiteSession("conversation_store")

  print("Welcome to the tutor chat! (type 'exit' to quit)")
  print("---------------------------------")
  name = input("Enter your name: ")
  interest = input("What are you interested in? ")

  context = {
   "name":name,
   "topic": interest
  }
  while True:
   user_input = input("Enter your prompt : ")
   if user_input == "exit":
    break
  
   result = Runner.run_streamed(
    starting_agent= personal_assistant,
    input=user_input,
    session = session,
    context=context
)
 
   async for event in result.stream_events():
    if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
     print(event.data.delta)

print()

asyncio.run(main())
