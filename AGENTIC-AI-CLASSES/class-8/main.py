from agents import Agent, handoff, RunContextWrapper, Runner, function_tool
from pydantic import BaseModel
import asyncio
from configure.config import gemini_model


class calc(BaseModel):
    n1: int
    n2: int

class User(BaseModel):
    user_role:str #admin, user

def enable_tool(ctx:RunContextWrapper[User], agent: Agent[User]):
    if ctx.context.user_role == "admin":
        return True
    return False

@function_tool(is_enabled=False)
def subtract(num:calc):
    print("subtracting..")
    """This tool is use for subtraction of the numbers"""
    return f"The answer is {num.n1 - num.n2}"


@function_tool()
def Add(num:calc):
    print("adding..")
    """This tool is use for Addition of the numbers"""
    return f"The answer is {num.n1 + num.n2}"


math_tutor = Agent(
    name = "Maths Assistant",
    instructions="You are an expert math assistant",
    model= gemini_model,
    tools=[Add, subtract],
    
)
physics_tutor = Agent(
    name = "physics Assistant",
    instructions="You are an expert physics assistant",
    model= gemini_model,
)

tutor = Agent(
    name="general tutor",
    instructions= "helpful agent",
    model=gemini_model,
    handoffs=[math_tutor, physics_tutor]
)
async def main():
  
   user = User("admin")
   result = Runner.run(
    starting_agent=math_tutor,
    input="add two plus 50 and then subtract 7 to the final answer ",
    stop_at_tool_names=["Add"],
    context=user 

)
   print(result.final_output)

asyncio.run(main())