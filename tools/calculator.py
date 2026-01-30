def run(input_data: str) -> str:
    """
    Simple calculator tool.
    Expects a math expression as string.
    """
    try:
        result = eval(input_data)
        return str(result)
    except Exception as e:
        return f"calculator error: {str(e)}"
