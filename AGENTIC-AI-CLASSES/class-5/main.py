from agents import Runner
import asyncio
from agentt.agent1 import TutorAgent

async def main():

 result = await Runner.run(
  starting_agent = TutorAgent,
  input="nine + nine"
  
    )
 print(result.final_output)
 

asyncio.run(main())