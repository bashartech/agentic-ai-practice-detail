from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig, set_default_openai_client, set_default_openai_api, set_tracing_disabled, function_tool
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

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

math_teacher = Agent(
    name = "Maths Tutor",
    instructions = " You are an expert maths tutor with 30 plus years of experience in teaching of maths and having phd in maths",
)

@function_tool
def getWeather(city: str):
    """ get the weather of city"""
    print("search for weather")
    return f"The weather of {city} is -10°C"

@function_tool
def getCurrencyRate(Currency: str):
    """get the currency rate"""
    print("search for currency rate")
    return f"The rate {Currency} is 1000$"


agent = Agent(
    name = "Helper Assistant",
    instructions="you are a helpful general agent",
    tools=[getWeather, getCurrencyRate]
)

prompt = input("Enter your prompt : ")

result = Runner.run_sync(
    agent,
    input = prompt,
    run_config=configure,
    max_turns=20
)

print(result.final_output)
