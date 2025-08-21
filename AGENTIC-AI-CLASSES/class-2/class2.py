from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig
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
MODEL = OpenAIChatCompletionsModel(
    model = gemini_model,
    openai_client = client
)

configure = RunConfig(
    model= MODEL,
    model_provider= client,
    tracing_disabled= True
)

math_teacher = Agent(
    name = "Maths Tutor",
    instructions = " You are an expert maths tutor with 30 plus years of experience in teaching of maths and having phd in maths",
    model = MODEL
)

result = Runner.run_sync(
    math_teacher,
    input = "2 + 2",
    run_config=configure
)

print(result.final_output)
