from agents import function_tool, RunContextWrapper
from data_file.data_file import UserSchema

@function_tool
def plus(ctx:RunContextWrapper[UserSchema], n1, n2):
    print("plus karo")
    return f"{ctx.context.name} aapka answer {n1 + n2} he"


@function_tool
def userData(ctx:RunContextWrapper[UserSchema]):
    print("data process")
    return f"{ctx.context.name} with an age of  {ctx.context.age} he"


@function_tool
def userDetail(name: str, age: int):
    return f"Name: {name}, Age: {age}"
