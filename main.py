import os
import json
from dotenv import load_dotenv
from groq import Groq
from utils.validator import validate_plan
from executor.tool_executor import execute_tool
from memory.execution_memory import ExecutionMemory



# ENVIRONMENT SETUP

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

client = Groq(api_key=api_key)



# LOAD SYSTEM PROMPT


with open("prompts/planner.txt", "r") as f:
    system_prompt = f.read()



# USER INPUT

user_input = input("Enter your task: ")


# AGENT LOOP (PLAN + VALIDATE)

MAX_RETRIES = 3
attempt = 0
success = False

schema_path = "schemas/plan_schema.json"

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_input}
]

while attempt < MAX_RETRIES:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.2
    )

    output_text = response.choices[0].message.content

    # ---- JSON PARSE CHECK ----
    try:
        parsed = json.loads(output_text)
    except json.JSONDecodeError:
        messages.append({
            "role": "system",
            "content": "Your previous response was NOT valid JSON. "
                       "Return ONLY valid JSON strictly following the schema."
        })
        attempt += 1
        continue

    # ---- SCHEMA VALIDATION ----
    is_valid, error_msg = validate_plan(parsed, schema_path)
    if not is_valid:
        messages.append({
            "role": "system",
            "content": f"Schema error: {error_msg}. "
                       "Fix the JSON to strictly match the schema."
        })
        attempt += 1
        continue



    # ---- SUCCESS ----
    print("\n✅ VALID PLAN GENERATED\n")
    print(json.dumps(parsed, indent=2))
    success = True
    break

else:
    print("❌ Failed to generate valid output after 3 attempts.")

if not success:
    exit(1)



# TOOL EXECUTION LOOP

memory = ExecutionMemory()



for step in parsed["steps"]:
    tool = step["tool_required"].lower().strip()
    tool_input = step["tool_input"].strip()

    if tool == "none":
        continue

    if memory.has(tool, tool_input):
        print(f"\n♻️ Reusing cached result for {tool}")
        result = memory.get(tool, tool_input)
    else:
        print(f"\n🔧 Executing tool: {tool}")
        result = execute_tool(tool, tool_input)
        memory.store(tool, tool_input, result)

    print("Tool output:", result)

