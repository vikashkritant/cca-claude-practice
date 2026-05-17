import json
import os
from dotenv import load_dotenv
import re

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")


def extract_json(text):
    """
    Extracts first JSON object from LLM response
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else None


def get_next_step(client, user_input, history):
    system_prompt = """
    You are a smart reasoning agent.

    You solve problems step-by-step using tools.

    Available tools:
    - add_numbers(a:int, b:int)
    - multiply_numbers(a:int, b:int)

    Rules:
    - You may use previous results from history
    - Be logical and efficient
    - If solved, return:

    {"final_answer": "answer"}

    Otherwise return:

    {
        "tool": "...",
        "args": {...}
    }
    """

    messages = [
        {"role": "user", "content": f"Problem: {user_input}"}
    ]

    for step in history:
        messages.append({
            "role": "assistant",
            "content": str(step)
        })

    response = client.messages.create(
        model=MODEL_NAME,
        system=system_prompt,
        messages=messages,
        max_tokens=150,
        temperature=0
    )

    return response.content[0].text


def parse_step(raw):
    """
    Parse single step JSON
    """
    clean = extract_json(raw)

    if not clean:
        raise ValueError(f"No JSON found in response:\n{raw}")

    return json.loads(clean)