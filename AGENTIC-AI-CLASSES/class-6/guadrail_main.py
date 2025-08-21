from pydantic import BaseModel
from agents import Agent, GuardrailFunctionOutput, RunContextWrapper, Runner, input_guardrail, output_guardrail, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered

from configure.config import gemini_model
import asyncio

class MessageOutput(BaseModel): 
    response: str


class input_output(BaseModel):
    isHistory: bool
    reason: str
    isPolitical: bool

guardrail_agent = Agent(
    name = "Guadrail Check",
    instructions="Check if the content is history-related and if it is political. "
                 "Return booleans for isHistory and isPolitical, plus a reason.",
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
        tripwire_triggered= final_output.isPolitical
    )

@input_guardrail
async def check_input(ctx:RunContextWrapper, agent:Agent, input_data:str):
    result = await Runner.run(
        guardrail_agent, input_data, context=ctx.context
    )
    final_output: input_output = result.final_output
    return GuardrailFunctionOutput(
        output_info= final_output.reason,
        tripwire_triggered= not final_output.isHistory
    )


agent = Agent(
    name="Hostory Agent",
    instructions="You are a History agent",
    model=gemini_model,
    input_guardrails=[check_input],
    output_type=MessageOutput,
    output_guardrails=[check_output]
)

async def main():
    try:
        prompt = input("Enter a prompt : ")
        msg = await Runner.run(
            starting_agent=agent,
            input= prompt
        )
        print(msg.final_output)
    except (InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered) as e:
        print("something wrong")


asyncio.run(main())
