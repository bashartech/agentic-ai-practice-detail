from agents import Agent, Runner, RunConfig, set_default_openai_client, set_default_openai_api, set_tracing_disabled, function_tool
import requests
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_base_url = os.getenv("GEMINI_BASE_URL")
gemini_model = os.getenv("GEMINI_MODEL")
weather_api_key = os.getenv("WEATHER_API_KEY")
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

@function_tool
def getWeather(city: str):
    """Get the current weather of a city"""
    print("search for {city}")
    url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}"

    try:
        response = requests.get(url)
        data = response.json()

        if "error" in data:
            return f"Error: {data['error']['message']}"
        
        location = data["location"]["name"]
        country = data["location"]["country"]
        temp_c = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        feelslike_c = data["current"]["feelslike_c"]

        return (
            f"The current weather in {location}, {country} is {temp_c}°C "
            f"with {condition}. Feels like {feelslike_c}°C."
        )

    except Exception as e:
        return f"Error fetching weather: {str(e)}"

agent = Agent(
    name = "Weather Agent",
    instructions="you are a helpful weather info agent, who use tools for response",
    tools=[getWeather]
)

prompt = input("Enter your prompt : ")

result = Runner.run_sync(
    agent,
    input = prompt,
    run_config=configure,
    max_turns=20
)

print(result.final_output)
