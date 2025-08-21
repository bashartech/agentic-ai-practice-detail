from agents import Runner, SQLiteSession
from agentz.agents_tutor import tutor
import asyncio
from openai.types.responses import ResponseTextDeltaEvent

async def main():
  
  agent_builder = {"name" : "M.Bashar Sheikh", "age" : 19}
 
  session = SQLiteSession("conversation_store")
  print("Welcome to the tutor chat! (type 'exit' to quit)")
  while True:
   user_input = input("Enter your prpmpt: ")
   if user_input == "exit":
    break
  
   result = Runner.run_streamed(
    starting_agent= tutor,
    input=user_input,
    session = session,
    context = agent_builder
)
 
   async for event in result.stream_events():
    if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
     print(event.data.delta)

print()

asyncio.run(main())
