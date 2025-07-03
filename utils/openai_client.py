import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env")

openai_client = OpenAI(api_key=api_key)

# List of allowed models by priority
DEFAULT_MODEL = "gpt-4o-mini"

def ask_openai(messages, model=DEFAULT_MODEL):
    response = openai_client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.5,  # Moderate randomness
    )
    return response.choices[0].message.content
