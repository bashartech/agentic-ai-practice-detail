from pydantic import BaseModel
from agents import Agent, GuardrailFunctionOutput, RunContextWrapper, Runner, output_guardrail,OutputGuardrailTripwireTriggered
from configure.config import gemini_model
import asyncio

class MessageOutput(BaseModel): 
    response: str

class Maths_Output(BaseModel):
    isMath: bool
    reason: str

guardrail_agent = Agent(
    name = "Guadrail Check",
    instructions="Check if the output includes any math.",
    model=gemini_model,
    output_type=Maths_Output

)

@output_guardrail
async def check_output(ctx:RunContextWrapper, agent:Agent, output:MessageOutput):
    result = await Runner.run(
        guardrail_agent, output.response, context=ctx.context
    )
    final_output: Maths_Output = result.final_output
    return GuardrailFunctionOutput(
        output_info= final_output.reason,
        tripwire_triggered= final_output.isMath
    )


agent = Agent(
    name="Math Agent",
    instructions="You are a math agent",
    model=gemini_model,
    output_type=MessageOutput,
    output_guardrails=[check_output]

)


async def main():
    try:
        msg = await Runner.run(
            starting_agent=agent,
            input= "Hello, can you help me solve for x: 2x + 3 = 11?"
        )
        print(msg.final_output)
    except OutputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped")


asyncio.run(main())
