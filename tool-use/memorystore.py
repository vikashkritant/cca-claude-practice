# memory/memory_store.py

class MemoryStore:
    def __init__(self, max_messages=10):
        self.messages = []
        self.max_messages = max_messages

    def add_user_message(self, content):
        self.messages.append({"role": "user", "content": content})
        self._trim()

    def add_agent_message(self, content):
        self.messages.append({"role": "assistant", "content": content})
        self._trim()

    def get_messages(self):
        return self.messages

    def clear(self):
        self.messages = []

    def _trim(self):
        # Keep only last N messages
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]