from agents import Agent, Runner, RunConfig, set_default_openai_client, set_default_openai_api, set_tracing_disabled, function_tool, ModelSettings
from openai.types.responses import ResponseTextDeltaEvent
from pydantic import BaseModel
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
from dataclasses import dataclass
load_dotenv()
import asyncio

gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_base_url = os.getenv("GEMINI_BASE_URL")
gemini_model = os.getenv("GEMINI_MODEL")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")


client = AsyncOpenAI(
    api_key = gemini_api_key,
   base_url=gemini_base_url 
   )
set_default_openai_client(client)
set_default_openai_api("chat_completions")
set_tracing_disabled(True)


configure = RunConfig(
    model= gemini_model,
)

@dataclass
class car1Data:
    name: str
    model: int
    info: str

class motorData(BaseModel):
    name: str
    model: int
    info: str

class bikeData(BaseModel):
    name: str
    model: int
    info: str

async def main(): 
  car_agent = Agent(
    name="Car_assistant",
    instructions="You are a helpful car assistant",
    output_type = car1Data,
    model=gemini_model
)

  bike_agent = Agent(
    name="Bike_assistant",
    instructions="You are a helpful bike assistanat",
    output_type = bikeData,
    model=gemini_model
)
 
  motor_agent = Agent(
    name="Motor_assistant",
    instructions="You are a helpful motor assistanat and answer by using tools and other agents",
    output_type = motorData,
    model=gemini_model,
    tools = [car_agent.as_tool(
       tool_name = "Car_assistant",
       tool_description="helpful car assistanat"
    ), bike_agent.as_tool(
        tool_name = "Bike_assistant",
       tool_description="helpful bike assistanat"
    )],
    handoffs=[car_agent, bike_agent],
    model_settings= ModelSettings(
       tool_choice="auto"
    )
)
 
 
  result = Runner.run_streamed(
    starting_agent=motor_agent,
    input = "Tell me about audi cars in detail",
)

  async for event in result.stream_events():
    if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
     print(event.data.delta)

asyncio.run(main())