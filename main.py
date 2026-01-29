import os
import json
from dotenv import load_dotenv
from groq import Groq

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

# 5. Call the model
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ],
    temperature=0.2
)

# 6. Get model output
output_text = response.choices[0].message.content

# 7. Try parsing JSON (single attempt only)
try:
    parsed = json.loads(output_text)
    print(json.dumps(parsed, indent=2))
except json.JSONDecodeError:
    print("❌ Invalid JSON output:")
    print(output_text)

