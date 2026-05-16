import json
import os
from dotenv import load_dotenv
import re

load_dotenv()
# Read variables
MODEL_NAME = os.getenv("MODEL_NAME")

def extract_json(text):
    match = re.search(r"\[.*\]", text, re.DOTALL)
    return match.group(0) if match else None

def create_plan(client, user_input):
    system_prompt = """
    You are a planning agent.

    Return ONLY a valid JSON array.
    No text. No explanation.

    Each step must have:
    - "tool"
    - "args"

    Available tools:
    add_numbers(a:int, b:int)

    Rules:
    - Use ONLY add_numbers
    - Do NOT solve the full problem
    - Break into steps
    - Use "$prev" to refer to previous step result
    """

    response = client.messages.create(
        model=MODEL_NAME,
        system=system_prompt,
        messages=[{"role": "user", "content": user_input}],
        max_tokens=100,
        temperature=0
    )

    return response.content[0].text
    

def parse_plan(raw):
    clean = extract_json(raw)

    if not clean:
        raise ValueError(f"No JSON found in response:\n{raw}")

    return json.loads(clean)