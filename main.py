import os
import json
from dotenv import load_dotenv
from groq import Groq
from utils.validator import validate_plan


# 1. Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

# 2. Initialize Groq client
client = Groq(api_key=api_key)



# 3. Load system prompt
with open("prompts/planner.txt", "r") as f:
    system_prompt = f.read()



# 4. Take user input
user_input = input("Enter your task: ")


# 5. Interaction loop with validation

MAX_RETRIES = 3
attempt = 0
schema_path = "schemas/plan_schemas.json"

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

    # 1️⃣ JSON parse check
    try:
        parsed = json.loads(output_text)
    except json.JSONDecodeError:
        messages.append({
            "role": "system",
            "content": "Your previous response was NOT valid JSON. Return ONLY valid JSON strictly following the schema."
        })
        attempt += 1
        continue

    # 2️⃣ Schema validation
    is_valid, error_msg = validate_plan(parsed, schema_path)
    if not is_valid:
        messages.append({
            "role": "system",
            "content": f"Schema error: {error_msg}. Fix the JSON to strictly match the schema."
        })
        attempt += 1
        continue

    # ✅ SUCCESS
    print(json.dumps(parsed, indent=2))
    break

else:
    print("❌ Failed to generate valid output after 3 attempts.")

