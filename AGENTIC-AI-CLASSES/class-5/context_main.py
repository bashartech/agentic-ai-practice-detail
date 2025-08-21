from pydantic import BaseModel
from agents import Runner, RunContextWrapper, function_tool, Agent
from configure.config import gemini_model
import asyncio
from agentt.agent1 import ContextAgent
from data_file.data_file import UserSchema, user1

async def main():
 
 structured_input = UserSchema(name="Ali", age=22)
 wrapped_context = RunContextWrapper(context=user1)

 result = await Runner.run(
  starting_agent = ContextAgent,
  input= "Tell me the users name and age from the data available in the context using the userData tool."
,
  context= wrapped_context
  
    )
 print(result.final_output)
 

asyncio.run(main())


# class UserSchema(BaseModel):
#     name: str
#     age: int

# class RunContextWrapper(BaseModel):
#     context: UserSchema

# @function_tool
# def userData(ctx: RunContextWrapper):
#     print("✅ userData tool was called!")
#     return f"{ctx.context.name} with an age of {ctx.context.age} he"

# ContextAgent = Agent(
#     name="Assistant agent",
#     instructions="You are data provider assistant agent",
#     model=gemini_model,
#     tools=[userData],  # tool is available
# )

# user1 = UserSchema(name="Hafeez", age=20)
# wrapped_context = RunContextWrapper(context=user1)

# result = Runner.run_sync(
#     starting_agent=ContextAgent,
#     input="Can you tell me the name and age of the user from the userData tool?",
#     context=wrapped_context
# )

# print(result.final_output)
