from tools import calculator, file_reader

TOOL_REGISTRY = {
    "calculator": calculator.run,
    "file_reader": file_reader.run
}

def execute_tool(tool_name: str, input_data: str) -> str:
    if tool_name not in TOOL_REGISTRY:
        return f"Unknown tool: {tool_name}"

    tool_fn = TOOL_REGISTRY[tool_name]
    return tool_fn(input_data)
