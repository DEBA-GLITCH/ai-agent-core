import json
from jsonschema import validate, ValidationError

def validate_plan(plan: dict, schema_path: str) -> tuple[bool, str]:
    with open(schema_path, "r") as f:
        schema = json.load(f)

    try:
        validate(instance=plan, schema=schema)
        return True, ""
    except ValidationError as e:
        return False, e.message
