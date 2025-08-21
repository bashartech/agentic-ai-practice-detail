from agents import Runner
import asyncio
from agent.agentss import info_agent
async def main():

    result = await Runner.run(
        starting_agent= info_agent,
        input="give user info through dynamic instructions of the agent",
        context={"name": "Bashar", "age": 19, "role":"Doctor"}
    )

    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())