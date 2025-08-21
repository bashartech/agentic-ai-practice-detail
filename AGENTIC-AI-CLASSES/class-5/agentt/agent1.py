from agents import Agent, handoff, function_tool,RunContextWrapper
from configure.config import gemini_model
from agents.extensions import handoff_filters
from func_tool.context_toolz import userData, plus, userDetail
from data_file.data_file import UserSchema, user1


@function_tool
def add(n1, n2):
    print("adding in process...")
    return f"Your answer is {n1 + n2}"
    


def on_handoff(context):
    print("maths agent activated")


mathsAgent = Agent(
        name="Maths Agent",
        instructions="You are an expert physics and maths agent",
        model = gemini_model,
        tools=[add],
    )

python_handoff = handoff(
    agent= mathsAgent,
    on_handoff= on_handoff,
    input_filter= handoff_filters.remove_all_tools # it will remove history of these tools

)

TutorAgent = Agent(
        name="All Subjects Agent",
        instructions="You are an expert Maths and Physics agent",
        model = gemini_model,
        handoffs=[python_handoff]
    )


ContextAgent = Agent(
        name="Assistant agent",
        instructions="You are data provider assistant agent",
        model = gemini_model,
        tools=[userData], # local level way to add data by passing as tool
    )


# restudy on that

# def on_handoffContaxt(ctx:RunContextWrapper[UserSchema], input_data: UserSchema): # latest way
#     print("Context agent activated")
#     return f"{input_data}"

# context_handoff = handoff(
#     agent= ContextAgent,
#     on_handoff=on_handoffContaxt,
#     input_filter= handoff_filters.remove_all_tools, # it will remove history of these tools
#     input_type = UserSchema

# )

# ContextAssistant = Agent(
#         name="AI Assistant ",
#         instructions="You are an assistant agent",
#         model = gemini_model,
#         handoffs=[context_handoff]
#     )