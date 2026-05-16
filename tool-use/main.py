from anthropic import Anthropic
from dotenv import load_dotenv
import os
from runmockagent import run_mock_agent
from runagent import run_agent
from memorystore import MemoryStore

# main.py

def load_prompt():
    with open("prompts/master_prompt.txt", "r") as f:
        return f.read()


def main():
    system_prompt = load_prompt()
    memory = MemoryStore()

    print("Agent is ready! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

         # Call agent
        print("DEBUG → Calling agent...")
        response = run_agent(user_input, system_prompt, memory)

        # Store response
        print("\n💾 DEBUG → Saving to memory:")
        print("User:", user_input)
        print("Agent:", response)
        print("="*50)
        memory.add_agent_message(response)

        print("Agent:", response)


if __name__ == "__main__":
    main()