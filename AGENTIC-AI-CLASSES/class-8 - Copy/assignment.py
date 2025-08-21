
from agents import Agent, handoff, RunContextWrapper, Runner, function_tool, ToolsToFinalOutputFunction,ModelSettings, input_guardrail, output_guardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
from pydantic import BaseModel
import asyncio
from configure.config import gemini_model

class MessageOutput(BaseModel): 
    response: str


class input_output(BaseModel):
    isUnEthical: bool
    reason: str

@function_tool
def get_order_status(order_id): 
    return order_id

guardrail_agent = Agent(
    name = "Guadrail Check",
    instructions="Check if the content contain any unethical or sentiment so not proceeded it",
    model=gemini_model,
    output_type=input_output

)

@output_guardrail
async def check_output(ctx:RunContextWrapper, agent:Agent, output:MessageOutput):
    result = await Runner.run(
        guardrail_agent, output.response, context=ctx.context
    )
    final_output: input_output = result.final_output
    return GuardrailFunctionOutput(
        output_info= final_output.reason,
        tripwire_triggered= final_output.isUnEthical
    )

@input_guardrail
async def check(ctx:RunContextWrapper, agent:Agent, input_data:str):
    result = await Runner.run(
        guardrail_agent, input_data, context=ctx.context
    )
    final_output: input_output = result.final_output
    return GuardrailFunctionOutput(
        output_info= final_output.reason,
        tripwire_triggered= final_output.isUnEthical
    )


class User(BaseModel):
    user_querey:str #about product and order

def enable_tool(ctx:RunContextWrapper[User], agent: Agent[User]):
    if ctx.context.user_querey == "order" or "product":
        return True
    return False


@function_tool(is_enabled=enable_tool)
def faq():
    return "our website having great rating of the products and this e commerce platform available 24 by 7 to sell quality prosucts. All brands are available in reasonable price"

human_agent = Agent(
    name="Human Agent",
    instructions="Answer the quieries of the customers and handle complex and sentiment queries",
    model=gemini_model
)

customer_support_bot_agent = Agent(
    name = "Customer Supprt Bot",
    instructions="""
- Answer the questions of the customers and if question in related to the sensitive and specific information so handsoff to the human agent.
- answer the question using information from the FAQ tool.
- if sentiment present so handoff to human agent
""",
model=gemini_model,
handoffs=[human_agent],
tools=[faq],
model_settings=ModelSettings(tool_choice="auto"),
input_guardrails=[check],
output_guardrails=[check]
)

async def main():
    try:
        prompt = input("Enter a prompt : ")
        msg = await Runner.run(
            starting_agent=customer_support_bot_agent,
            input= prompt
        )
        print(msg.final_output)
    except (InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered) as e:
        print("something wrong")


asyncio.run(main())
