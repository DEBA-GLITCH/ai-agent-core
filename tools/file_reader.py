def run(input_data: str) -> str:
    """
    Reads a text file and returns its content.
    input_data = file path
    """
    try:
        with open(input_data, "r") as f:
            return f.read()
    except Exception as e:
        return f"File read error: {str(e)}"
