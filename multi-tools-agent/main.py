from planner import get_next_step, parse_step
from executor import execute_step
import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv()

API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

client = Anthropic(api_key=API_KEY)


def run():
    user_input = input("You: ")

    history = []       # 🧠 stores all steps
    result = None      # 🔁 stores last result

    while True:
        # 🔮 Ask LLM for next step
        step_text = get_next_step(client, user_input, history)
        print("\n🧠 RAW STEP:\n", step_text)

        # 🧾 Parse JSON
        step = parse_step(step_text)

        # ✅ If final answer → stop
        if "final_answer" in step:
            print("\n✅ Final Answer:", step["final_answer"])
            break

        # 🔧 Execute tool
        result = execute_step(step, result)

        print("Result:", result)

        # 🧠 Save to history
        history.append({
            "step": step,
            "result": result
        })


if __name__ == "__main__":
    run()