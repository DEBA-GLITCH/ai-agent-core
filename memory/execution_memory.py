class ExecutionMemory:
    def __init__(self):
        self.cache = {}

    def has(self, tool_name: str, tool_input: str) -> bool:
        key = (tool_name, tool_input)
        return key in self.cache

    def get(self, tool_name: str, tool_input: str) -> str:
        return self.cache[(tool_name, tool_input)]

    def store(self, tool_name: str, tool_input: str, output: str):
        key = (tool_name, tool_input)
        self.cache[key] = output

    def clear(self):
        self.cache = {}
        