from pydantic import BaseModel
from agents import RunContextWrapper, function_tool

class AgentBuilderSchema(BaseModel):
    name: str
    age: int

@function_tool
def agent_builder(ctx:RunContextWrapper[AgentBuilderSchema]):
    """You can tell the informaion about the owner of this agent"""
    return f"The name of the owner of this agent is {ctx.context['name']} and his age is {ctx.context['age']}."
