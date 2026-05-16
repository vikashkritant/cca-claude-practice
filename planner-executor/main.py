from planner import create_plan, parse_plan
from executor import execute_plan
import os
from dotenv import load_dotenv
# your Claude client init here
from anthropic import Anthropic

# Load .env
load_dotenv()

# Read variables
API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

client = Anthropic(api_key=API_KEY)

def run():
    user_input = input("You: ")

    plan_text = create_plan(client, user_input)

    print("\n🧠 RAW PLAN:\n", plan_text)
    plan = parse_plan(plan_text)

    if plan:
        final_result = execute_plan(plan)
        print("\n✅ Final Answer:", final_result)
    else:
        print("❌ Plan failed")

if __name__ == "__main__":
    run()