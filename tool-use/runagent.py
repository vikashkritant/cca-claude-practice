# run_agent.py
import os
import anthropic
from dotenv import load_dotenv
from tools.basic_tools import add_numbers, get_current_topic

# Load .env
load_dotenv()

# Read variables
API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

client = anthropic.Anthropic(api_key=API_KEY)

tools = [
    {
        "name": "add_numbers",
        "description": "Add two numbers",
        "input_schema": {
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": "integer"}
            },
            "required": ["a", "b"]
        }
    },
    {
        "name": "get_current_topic",
        "description": "Get current study topic",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    }
]

def run_agent(user_input, system_prompt, memory):
    messages = []

    # Add memory
    for msg in memory.get_messages():
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    # Add current input
    messages.append({
        "role": "user",
        "content": user_input
    })

    step = 0
    MAX_STEPS = 5   # 🔥 prevents infinite loops

    while step < MAX_STEPS:
        step += 1

        print(f"\n🧠 STEP {step}")

        response = client.messages.create(
            model=MODEL_NAME,
            system=system_prompt,
            messages=messages,
            tools=tools,
            max_tokens=120,
            temperature=0.2
        )

        # 🔹 Check if tool is used
        if response.stop_reason == "tool_use":
            print("🔧 Tool requested")

            # Append assistant tool call
            messages.append({
                "role": "assistant",
                "content": response.content
            })

            # Handle ALL tool calls (future-proof)
            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    tool_use_id = block.id

                    print("Tool:", tool_name)
                    print("Input:", tool_input)

                    # Execute tool
                    if tool_name == "add_numbers":
                        result = add_numbers(**tool_input)

                    elif tool_name == "get_current_topic":
                        result = get_current_topic()

                    else:
                        result = "Unknown tool"

                    print("Result:", result)

                    # Send result back
                    messages.append({
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": str(result)
                        }]
                    })

            continue  # 🔥 go to next loop iteration

        # 🔹 Final answer
        else:
            final_text = response.content[0].text

            print("✅ Final Answer Reached")
            return final_text

    return "⚠️ Max steps reached without final answer."