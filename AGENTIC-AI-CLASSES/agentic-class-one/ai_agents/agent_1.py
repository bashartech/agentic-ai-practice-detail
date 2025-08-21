from configuration.conf import MODEL
from agents import Agent

math_teacher = Agent(
    name = "Maths Tutor",
    instructions = " You are an expert maths tutor with 30 plus years of experience in teaching of maths and having phd in maths",
    model = MODEL
)
