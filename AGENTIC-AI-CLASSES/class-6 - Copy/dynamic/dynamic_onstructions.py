from agents import  RunContextWrapper, function_tool

@function_tool
def dynamic_instruction(ctx:RunContextWrapper, agent):
    """provide data of the users"""
    print(agent)
    return f"User name is {ctx.context['name']} and age is {ctx.context['age']} he is an expert {ctx.context['role']}"
