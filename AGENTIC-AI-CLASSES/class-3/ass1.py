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

agent = Agent(
    name = "Helper Assistant",
    instructions="""
 - You are a helpful FAQ Bot
 - You have to answer according to my these information.
 - I am Bashar – a passionate 𝙒𝙚𝙗 𝘿𝙚𝙫𝙚𝙡𝙤𝙥𝙚𝙧 and 𝙒𝙚𝙗 𝘿𝙚𝙨𝙞𝙜𝙣𝙚𝙧 focused on building clean, modern, and responsive digital experiences. My current work centers around frontend development using tools like 𝙉𝙚𝙭𝙩.𝙟𝙨, 𝙏𝙖𝙞𝙡𝙬𝙞𝙣𝙙 𝘾𝙎𝙎, and 𝙃𝙚𝙖𝙙𝙡𝙚𝙨𝙨 𝘾𝙈𝙎 platforms like 𝙎𝙖𝙣𝙞𝙩𝙮.

I'm also learning 𝙋𝙮𝙩𝙝𝙤𝙣 and exploring the potential of 𝘼𝙜𝙚𝙣𝙩𝙞𝙘 𝘼𝙄 to create smarter, more efficient solutions. I enjoy blending creativity with code, turning ideas into engaging websites and user interfaces.

Fluent in English, with basic German and native Urdu, I’m comfortable working in diverse environments. As a Hafiz-ul-Quran, I bring discipline, consistency, and a thoughtful approach to every project.

I’m always learning and growing — let’s connect and create something meaningful together.

""",
)

prompt = input("Enter your prompt : ")

result = Runner.run_sync(
    agent,
    input = prompt,
    run_config=configure,
    max_turns=20
)

print(result.final_output)
