from agents import Agent, handoff, RunContextWrapper, Runner, function_tool, ToolsToFinalOutputFunction
from pydantic import BaseModel
import asyncio
from configure.config import gemini_model


class calc(BaseModel):
    n1: int
    n2: int

async def stop_at_error_tool(ctx:RunContextWrapper, tool_result: list[ToolsToFinalOutputFunction]):
    return ToolsToFinalOutputFunction(
        isfinalOutput = True, final_output = tool_result[0].output
    )

@function_tool(is_enabled=False)
def subtract(num:calc):
    print("subtracting..")
    """This tool is use for subtraction of the numbers"""
    return f"The answer is {num.n1 - num.n2}"


@function_tool(failure_error_function= None)
def Add(num:calc):
    print("adding..")
    """This tool is use for Addition of the numbers"""
    return f"The answer is {(num.n1 + num.n2) / 0}",
   


math_tutor = Agent(
    name = "Maths Assistant",
    instructions="You are an expert math assistant",
    model= gemini_model,
    tools=[Add, subtract], 
    tool_use_behavior=stop_at_error_tool   
)
async def main():
  
   result = Runner.run(
    starting_agent=math_tutor,
    input="add two plus 50 and then subtract 7 to the final answer ",
     

)
   print(result.final_output)

asyncio.run(main())