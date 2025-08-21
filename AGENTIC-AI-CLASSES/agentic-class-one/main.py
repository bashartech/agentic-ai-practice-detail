from agents import Runner
import asyncio
from configuration.conf import configure
from ai_agents.agent_1 import math_teacher

async def main():
    result = await Runner.run(
        math_teacher,
        input = "Explain integration in baby steps",
        run_config=configure
    )
    print(result.final_output)
asyncio.run(main())
