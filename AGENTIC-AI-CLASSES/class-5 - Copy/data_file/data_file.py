from pydantic import BaseModel

class UserSchema(BaseModel):
    name:str
    age: int
    work: str

class RunContextWrapper(BaseModel):
    context: UserSchema

user1 = UserSchema(
    name = "Bashar",
    age = 19,
    work = "building an open ai and also help to build groq and meta. all are build by me"
)
