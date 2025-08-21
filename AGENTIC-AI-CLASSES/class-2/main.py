from agents import (
    Agent,  RunConfig, set_default_openai_client,
    set_default_openai_api, set_tracing_disabled, function_tool
)
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import smtplib
import json
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_base_url = os.getenv("GEMINI_BASE_URL")
gemini_model = os.getenv("GEMINI_MODEL")

# Email credentials
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

print(f"🔧 Config loaded - Model: {gemini_model}")
print(f"📧 Email configured: {EMAIL_ADDRESS}")

# Validate keys
if not gemini_api_key or not gemini_base_url or not gemini_model:
    raise ValueError("Gemini config missing in .env")

if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    print("⚠️ Warning: Email credentials missing - email functionality will be disabled")

# Setup OpenAI-compatible client (for Gemini)
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=gemini_base_url
)

# Register the Gemini-compatible client with OpenAI Agent SDK
set_default_openai_client(client)
set_default_openai_api("chat_completions")
set_tracing_disabled(True)

# Define LLM config
configure = RunConfig(
    model=gemini_model
)

def extract_json_from_response(text: str) -> dict:
    """Extract JSON from Gemini response that might be wrapped in markdown"""
    try:
        # First try direct JSON parsing
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to extract JSON from markdown code blocks
        json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
        match = re.search(json_pattern, text, re.DOTALL)
        if match:
            json_str = match.group(1)
            return json.loads(json_str)
        
        # Try to find JSON-like structure without code blocks
        json_pattern2 = r'\{[^{}]*"email"[^{}]*"message"[^{}]*\}'
        match2 = re.search(json_pattern2, text, re.DOTALL)
        if match2:
            return json.loads(match2.group(0))
        
        raise ValueError(f"Could not extract valid JSON from: {text}")

# ---------------- EMAIL TOOL ----------------
@function_tool
async def sendEmail(prompt: str) -> str:
    """
    Extract email address and message from user prompt, then send email.
    The prompt should contain an email address and the message content.
    """
    print("🔄 Processing email request...")
    
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        return "❌ Email functionality is not configured. Please set EMAIL_ADDRESS and EMAIL_PASSWORD in .env file."
    
    # More specific system message for Gemini
    system_msg = """You are an email extraction tool. Your job is to extract the email address and message from the user's request.

IMPORTANT INSTRUCTIONS:
1. Find the email address in the user's request
2. Extract or compose the message content based on what the user wants to send
3. Return ONLY a valid JSON object in this exact format:
{"email": "recipient@example.com", "message": "The message content here"}

Do not include any other text, explanations, or markdown formatting.
Do not wrap the JSON in code blocks.
Return only the raw JSON object."""

    user_msg = f"""Extract the email and message from this request: {prompt}

Remember: Return only the JSON object, nothing else."""

    try:
        # Call Gemini via Agent SDK
        response = await client.chat.completions.create(
            model=gemini_model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.1  # Lower temperature for more consistent output
        )
        
        ai_content = response.choices[0].message.content.strip()
        print(f"📝 Raw LLM Output: {ai_content}")
        
        # Extract JSON from response
        parsed = extract_json_from_response(ai_content)
        print(f"✅ Parsed JSON: {parsed}")
        
        to_email = parsed.get("email", "").strip()
        message_body = parsed.get("message", "").strip()
        
        if not to_email or not message_body:
            return "❌ Error: Could not extract email address or message from the request."
        
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, to_email):
            return f"❌ Error: Invalid email format: {to_email}"
        
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = "Message from Bashar's AI Agent"
        
        # Add message body
        msg.attach(MIMEText(message_body, 'plain'))
        
        # Send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        
        return f"✅ Email sent successfully to {to_email}\n📧 Message: {message_body}"
        
    except json.JSONDecodeError as e:
        return f"❌ JSON parsing error: {str(e)}\nRaw response: {ai_content}"
    except Exception as e:
        return f"❌ Error sending email: {str(e)}"

@function_tool
def getWeather(city: str) -> str:
    """Get weather information for a city"""
    print(f"🌤️ Getting weather for {city}")
    return f"🌤️ The weather in {city} is 25°C with clear skies"

@function_tool
def getCurrencyRate(currency: str) -> str:
    """Get currency exchange rate"""
    print(f"💱 Getting currency rate for {currency}")
    return f"💱 The rate for {currency} is 300 PKR"

@function_tool
def calculate(expression: str) -> str:
    """Perform basic mathematical calculations"""
    try:
        # Simple and safe calculation
        result = eval(expression.replace("x", "*").replace("÷", "/"))
        return f"🧮 {expression} = {result}"
    except:
        return f"❌ Could not calculate: {expression}"

# Create the agent
agent = Agent(
    name="Smart Assistant",
    instructions="""You are a helpful smart assistant with the following capabilities:

1. **Email Sending**: When users want to send emails, use the sendEmail tool. Look for email addresses and message content in their requests.

2. **Weather**: Use getWeather tool when users ask about weather in specific cities.

3. **Currency**: Use getCurrencyRate tool when users ask about currency exchange rates.

4. **Calculations**: Use calculate tool for mathematical operations.

5. **General Questions**: Answer general questions directly.

IMPORTANT GUIDELINES:
- Always use the appropriate tool for the user's request
- For email requests, use the sendEmail tool
- For weather requests, use the getWeather tool  
- For currency requests, use the getCurrencyRate tool
- For math problems, use the calculate tool
- Be helpful, friendly, and conversational
- Always confirm successful actions to the user

Examples:
- "Send email to john@test.com saying hello" → use sendEmail tool
- "What's the weather in Paris?" → use getWeather tool
- "USD to PKR rate?" → use getCurrencyRate tool
- "What is 2 + 2?" → use calculate tool""",
    
    tools=[getWeather, getCurrencyRate, sendEmail, calculate]
)

print("✅ Agent initialized successfully")

# Export the agent and config for use in other files
__all__ = ['agent', 'configure']
