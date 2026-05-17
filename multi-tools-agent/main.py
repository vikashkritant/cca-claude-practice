import json
import re
from planner import get_next_step   # 🔥 use loop planner
from executor import execute_step
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

client = Anthropic(api_key=API_KEY)


def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else None


def run():
    user_input = input("You: ")

    history = []
    result = None

    for i in range(5):  # limit steps
        print(f"\n🔁 Step {i+1}")

        raw = get_next_step(client, user_input, history)
        print("🧠 RAW:", raw)

        clean = extract_json(raw)

        if not clean:
            print("❌ Failed to parse")
            break

        step = json.loads(clean)

        # ✅ final answer
        if "final_answer" in step:
            print("\n✅ Final Answer:", step["final_answer"])
            return

        # 🔧 execute step
        result = execute_step(step, result)
        print("Result:", result)

        # 🧠 store history
        history.append({
            "step": step,
            "result": result
        })

    print("\n⚠️ Max steps reached")


if __name__ == "__main__":
    run()