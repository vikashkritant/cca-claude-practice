from mockclaude import MockClaude
def run_mock_agent(prompt):
    claude = MockClaude()

    for i in range(3):  # max iterations (VERY IMPORTANT for exam)
        response = claude.send(prompt)

        print("\nStep:", i)
        print("Response:", response)

        if response["stop_reason"] == "end_turn":
            print("✅ Finished")
            break

        if response["stop_reason"] == "tool_use":
            print("🔧 Executing tool...")

            # simulate tool result
            tool_result = "4"

            # feed result back into loop
            prompt = f"tool result: {tool_result}"