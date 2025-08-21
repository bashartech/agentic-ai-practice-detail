from agents import Agent, Runner, RunContextWrapper, function_tool, input_guardrail, ModelSettings, GuardrailFunctionOutput, InputGuardrailTripwireTriggered
from pydantic import BaseModel
import asyncio
import random
from configure.config import gemini_model


@function_tool
async def get_flight_status(order_id: str):
    """Simulates fetching flight status"""
    fake_status = ["On Time", "Delayed", "Boarding", "Cancelled"]
    if order_id.startswith("FL"):
        return {"order_id": order_id, "status": random.choice(fake_status)}
    else:
        raise ValueError("Invalid flight ID")


@input_guardrail
async def check_language(ctx: RunContextWrapper, agent: Agent, user_input: str):
    bad_words = ["stupid", "idiot", "hate"]
    if any(word in user_input.lower() for word in bad_words):
        return GuardrailFunctionOutput(
            output_info="⚠️ Please keep the conversation respectful.",
            tripwire_triggered=True   # THIS stops execution
        )
    return GuardrailFunctionOutput(
        output_info="OK",
        tripwire_triggered=False
    )


def get_dynamic_instructions(user_location: str, sentiment: str):
    """Returns different instructions based on location & sentiment"""
    base = "You are a helpful travel assistant."

    if sentiment == "negative":
        base += " Speak in a calm and empathetic tone. Offer solutions."
    else:
        base += " Keep a friendly and energetic tone."

    if user_location == "airport":
        base += " Focus on gate info, boarding times, and flight delays."
    elif user_location == "home":
        base += " Give trip preparation tips and packing reminders."

    return base


bot_agent = Agent(
    name="TravelBot",
    instructions=get_dynamic_instructions(user_location="home", sentiment="positive"),
    tools=[get_flight_status],
    model=gemini_model,
    input_guardrails=[check_language],
    model_settings=ModelSettings(tool_choice="auto")
)

human_agent = Agent(
    name="HumanAgent",
    instructions="You are a human travel support agent. Handle escalated or complex cases.",
    model=gemini_model
)


async def main():
    sentiment = "negative"
    user_location = input("Whats your location: ")
    bot_agent.instructions = get_dynamic_instructions(user_location, sentiment)

    user_query = input("Enter your prompt: ")

    try:
        result = await Runner.run(
            starting_agent=bot_agent,
            input=user_query
        )
        print("Bot Output:", result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print("Guardrail Triggered")


asyncio.run(main())
