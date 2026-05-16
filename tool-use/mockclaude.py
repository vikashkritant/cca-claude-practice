class MockClaude:
    def __init__(self):
        self.call_count = 0

    def send(self, prompt):
        self.call_count += 1

        # Simulate different stop reasons
        if "calculate" in prompt:
            return {
                "content": "Calling calculator tool",
                "stop_reason": "tool_use",
                "tool": "calculator",
                "input": "2+2"
            }

        return {
            "content": "4",
            "stop_reason": "end_turn"
        }
