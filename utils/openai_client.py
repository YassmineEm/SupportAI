import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env")

openai_client = OpenAI(api_key=api_key)


DEFAULT_MODEL = "gpt-4o-mini"

def ask_openai(messages, model=DEFAULT_MODEL):
    response = openai_client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.5,  
    )
    return response.choices[0].message.content
