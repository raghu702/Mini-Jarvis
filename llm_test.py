import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

response = client.responses.create(
    model="gpt-6-luna",
    input="""
You are the language understanding component of Mini-Jarvis.

Understand the user's request and return ONLY valid JSON.

The JSON must have exactly this structure:

{
    "intent": "string",
    "entities": {
        "destination": "string or null",
        "date": "string or null"
    }
}

User request:
Repu Hyderabad ki train chudu
"""
)

print(response.output_text)