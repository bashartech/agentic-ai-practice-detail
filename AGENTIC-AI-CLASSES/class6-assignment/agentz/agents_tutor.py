from agents import Agent, handoff, RunContextWrapper
from configure.config import gemini_model
from toolz.toolz import subtract, Add, calc
from agents.extensions import handoff_filters
from local_context.local_context import agent_builder, AgentBuilderSchema
from toolz.toolz import user_context
from dynamic_context.dynamic_context import dynamic_instruction

def on_handoff(ctx:RunContextWrapper[None], input : calc):
    print("maths agent activated")


math_tutor = Agent(
    name = "Maths Assistant",
    instructions="You are an expert math assistant",
    model= gemini_model,
    tools=[subtract, Add]
)

math_handoff = handoff(
    agent=math_tutor,
    on_handoff=on_handoff,
    # input_filter= handoff_filters.remove_all_tools,
    input_type=calc
)


tutor = Agent[AgentBuilderSchema](
    name = "Tutor Assistant",
    instructions="""
- You are an expert Tutor of all the subject and answer by using specific tools and agents according to the question.
- You are a helpful tutor who remembers past conversations.
- You also tell the information about the owner of this agent
""",
    model= gemini_model,
    handoffs=[math_handoff],
    tools=[agent_builder]
)

personal_assistant = Agent(
    name="Personal_Assistant",
    instructions= dynamic_instruction,
    tools=[user_context],
    model= gemini_model,
)