from pydantic import BaseModel

class UserSchema(BaseModel):
    name:str
    age: int

class RunContextWrapper(BaseModel):
    context: UserSchema

user1 = UserSchema(
    name = "Hafeez",
    age = 20
)