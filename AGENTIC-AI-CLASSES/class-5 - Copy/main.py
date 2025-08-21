from agents import Runner, RunContextWrapper, function_tool, Agent
from configure.config import gemini_model
import asyncio
from data_file.data_file import UserSchema, user1

@function_tool
async def fetch_info(wrapper: RunContextWrapper[UserSchema]) -> str:
    """Fetch the information of the user. Call this function to get users information"""
    return f"The user {wrapper.context.name} is 19 years old and he is working {wrapper.context.work}"

async def main():

    info_agent = Agent[UserSchema](
        name = "assistant",
        tools=[fetch_info],
        model = gemini_model
    )
    result = await Runner.run(
        starting_agent= info_agent,
        input="What is the age of the user? and tell me about their work",
        context = user1
    )

    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())