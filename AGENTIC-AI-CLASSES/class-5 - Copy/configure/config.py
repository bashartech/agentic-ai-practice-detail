from dotenv import load_dotenv
load_dotenv()

from agents import RunConfig, set_default_openai_client, set_default_openai_api, set_tracing_disabled
from openai import AsyncOpenAI
import os

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
