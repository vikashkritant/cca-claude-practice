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


def get_next_step(client, user_input, previous_result=None):
    """
    Ask LLM for NEXT step (not full plan)
    """

    system_prompt = """
    You are a step-by-step reasoning agent.

    At each step, decide the NEXT action.

    Return ONLY one JSON object.

    Available tools:
    - add_numbers(a:int, b:int)
    - multiply_numbers(a:int, b:int)

    Rules:
    - Use "$prev" if referring to previous result
    - Think step-by-step
    - Do NOT skip steps
    - If problem is solved, return:

    {"final_answer": "answer here"}

    Otherwise return:

    {
        "tool": "tool_name",
        "args": {
            "a": ...,
            "b": ...
        }
    }
    """

    user_message = user_input

    # If we already have a result, pass it back
    if previous_result is not None:
        user_message += f"\nPrevious result: {previous_result}"

    response = client.messages.create(
        model=MODEL_NAME,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
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