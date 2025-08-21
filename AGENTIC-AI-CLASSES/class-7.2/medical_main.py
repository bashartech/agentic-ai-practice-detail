import asyncio
import aiohttp
from pydantic import BaseModel
from agents import Agent, Runner, RunContextWrapper, function_tool, input_guardrail, GuardrailFunctionOutput, ModelSettings
from configure.config import gemini_model 


@function_tool
async def get_drug_info(drug_name: str):
    print("Searching for best result")
    """Fetches drug label info from FDA API"""
    url = f"https://api.fda.gov/drug/label.json?search=openfda.generic_name:{drug_name}&limit=1"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise ValueError("Error fetching drug info")
            data = await resp.json()
            if "results" not in data:
                raise ValueError("Drug not found")
            return {
                "drug_name": drug_name,
                "purpose": data["results"][0].get("purpose", ["No purpose info"])[0],
                "warnings": data["results"][0].get("warnings", ["No warnings info"])[0]
            }


@function_tool
async def get_outbreak_news():
    print("Searching for best result")
    """Fetches latest WHO outbreak news"""
    url = "https://www.who.int/feeds/entity/csr/don/en/rss.xml"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise ValueError("Error fetching outbreak news")
            xml_text = await resp.text()
            # Just return raw XML for brevity — in real case, parse it
            return {"raw_rss": xml_text[:500] + "..."}  # preview


@input_guardrail
async def prevent_harmful_medical(ctx: RunContextWrapper, agent: Agent, user_input: str):
    dangerous_keywords = ["suicide", "self-harm", "overdose"]
    if any(word in user_input.lower() for word in dangerous_keywords):
        return GuardrailFunctionOutput(
            output_info="⚠️ This topic requires immediate professional help. Please contact a crisis helpline.",
            tripwire_triggered=True
        )
    return GuardrailFunctionOutput(output_info="OK", tripwire_triggered=False)


def detect_dynamic_instructions(prompt: str):
    """Analyzes user query and adjusts agent instructions dynamically."""
    prompt_lower = prompt.lower()
    base = "You are a helpful medical assistant. Always provide accurate, safe, evidence-based information."

    if "drug" in prompt_lower or "medicine" in prompt_lower or "tablet" in prompt_lower:
        base += " The user is asking about medication. Use the get_drug_info tool to provide FDA-approved details."
    elif "outbreak" in prompt_lower or "disease spread" in prompt_lower:
        base += " The user is asking about outbreaks. Use get_outbreak_news tool to provide WHO outbreak information."
    elif "symptom" in prompt_lower or "feel" in prompt_lower or "pain" in prompt_lower:
        base += " The user is describing symptoms. Give general safe advice and suggest professional consultation."
    else:
        base += " The topic is general health-related. Provide reliable public health information."

    return base


# ---------------------------
# AGENTS
# ---------------------------
bot_agent = Agent(
    name="MediBot",
    instructions="Placeholder — will be updated dynamically",
    tools=[get_drug_info, get_outbreak_news],
    model=gemini_model,
    input_guardrails=[prevent_harmful_medical],
    model_settings=ModelSettings(tool_choice="auto")
)


# ---------------------------
# MAIN FLOW
# ---------------------------
async def main():
    user_query = input("Ask your medical question: ")

    # Set instructions dynamically from query itself
    bot_agent.instructions = detect_dynamic_instructions(user_query)

    result = await Runner.run(
        starting_agent=bot_agent,
        input=user_query
    )

    if "⚠️" in str(result.final_output):
        print("Guardrail Triggered:", result.final_output)
    else:
        print("Bot Output:", result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
