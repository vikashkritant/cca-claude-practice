import json
from config import MODEL_NAME

def create_plan(client, user_input):
    system_prompt = """
    You are a planning agent.

    Return ONLY a JSON array of steps.

    Each step must have:
    - "tool"
    - "args"

    Do NOT solve the problem.
    """

    response = client.messages.create(
        model=MODEL_NAME,
        system=system_prompt,
        messages=[{"role": "user", "content": user_input}],
        max_tokens=100,
        temperature=0
    )

    plan_text = response.content[0].text

    print("\n🧠 RAW PLAN:\n", plan_text)

    return plan_text


def parse_plan(plan_text):
    try:
        return json.loads(plan_text)
    except Exception as e:
        print("❌ Invalid JSON:", e)
        return None