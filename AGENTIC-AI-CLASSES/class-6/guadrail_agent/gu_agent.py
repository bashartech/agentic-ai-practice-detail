from pydantic import BaseModel
from agents import Agent, GuardrailFunctionOutput, RunContextWrapper, Runner, input_guardrail, InputGuardrailTripwireTriggered
from configure.config import gemini_model

class Maths(BaseModel):
    isMath: bool
    reason: str

guardrail_agent = Agent(
    name = "Guadrail Check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=Maths

)

@input_guardrail
async def check_input(ctx:RunContextWrapper, agent:Agent, input_data:str):
    result = await Runner.run(
        guardrail_agent, input_data, context=ctx.context
    )
    final_output = result.final_output
    print(final_output)
    return GuardrailFunctionOutput(
        output_info= "hello world",
        tripwire_triggered= False
    )


agent = Agent(
    name="Math Agent",
    instructions="You are a math agent",
    model=gemini_model,
    input_guardrails=[check_input]

)


async def main():
    try:
        await Runner.run(
            starting_agent=agent,
            input= "Hello, can you help me solve for x: 2x + 3 = 11?"
        )
        print("Guardrail didn't trip - this is unexpected")
    except InputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped")

