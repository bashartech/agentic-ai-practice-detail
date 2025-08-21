from agents import  RunContextWrapper, function_tool

@function_tool
def plus(ctx:RunContextWrapper,n1, n2):
    """plus function"""
    print("plus tool..")
    print(f"User name is {ctx.context['name']} and age is {ctx.context['age']} he is an expert {ctx.context['role']}")
    return f"Your answer is {n1 + n2}"

@function_tool
def userInfo(ctx:RunContextWrapper):
    """provide user data to the agent and llm"""
    print("user info tool..")
    return f"User name is {ctx.context['name']} and age is {ctx.context['age']} he is an expert {ctx.context['role']}"