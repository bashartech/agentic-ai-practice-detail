from agents import Agent, RunContextWrapper
from configure.config import gemini_model
from toolsz.toolz import plus, userInfo
from dynamic.dynamic_onstructions import dynamic_instruction

info_agent = Agent(
        name = "user info agent",
        instructions=dynamic_instruction,
        model = gemini_model,
        tools=[plus]
    )