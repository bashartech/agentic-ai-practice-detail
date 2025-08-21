from agents import Runner, RunContextWrapper, function_tool, Agent
from configure.config import gemini_model
import asyncio
from data_file.data_file import UserSchema, user1

@function_tool
async def fetch_age(wrapper: RunContextWrapper[UserSchema]) -> str:
    """Fetch the age of the user. Call this function to get users age information"""
    return f"The user {wrapper.context.name} is 47 years old"

async def main():

    info_agent = Agent[UserSchema](
        name = "assistant",
        tools=[fetch_age],
        model = gemini_model
    )
    result = await Runner.run(
        starting_agent= info_agent,
        input="what is the age of the user",
        context = user1
    )

    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())