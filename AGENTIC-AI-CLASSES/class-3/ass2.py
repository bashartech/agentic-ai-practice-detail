from agents import Agent, Runner, RunConfig, set_default_openai_client, set_default_openai_api, set_tracing_disabled, function_tool
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

@function_tool
def mathTutor(a:int, b:int):
    print("solving maths question")
    return a + b , a - b, a * b, a / b

math_teacher = Agent(
    name = "Maths Tutor",
    instructions = " You are an expert maths tutor with 30 plus years of experience in teaching of maths and having phd in maths",
    tools=[mathTutor]
)


prompt = input("Enter your prompt : ")

result = Runner.run_sync(
    math_teacher,
    input = prompt,
    run_config=configure,
    max_turns=20
)

print(result.final_output)
