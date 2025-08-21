from agents import RunContextWrapper

def dynamic_instruction(ctx:RunContextWrapper, agent):
    name = ctx.context.get("name", "user")
    topic = ctx.context.get("topic", "AI")
    return f"You are a helpful AI assisting {name}, who is interested in {topic}"