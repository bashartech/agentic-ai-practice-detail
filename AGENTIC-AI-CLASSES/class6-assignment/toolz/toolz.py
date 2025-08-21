from agents import function_tool
from pydantic import BaseModel

class calc(BaseModel):
    n1: int
    n2: int



@function_tool(name_override="Subtraction_Tool", description_override="This tool use to subtract the numbers")
def subtract(num:calc):
    """This tool is use for subtraction of the numbers"""
    return f"The answer is {num.n1 - num.n2}"


@function_tool(name_override="Addition_Tool", description_override="This tool use to Add the numbers")
def Add(num:calc):
    """This tool is use for Addition of the numbers"""
    return f"The answer is {num.n1 + num.n2}"


@function_tool
def user_context(name: str, topic: str):
    """Sets username and topic of its interest"""
    return f"The name of the user is {name} and he like to know about {topic}"