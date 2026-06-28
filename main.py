import os
import json
import requests #requests → to call the API

from dotenv import load_dotenv #python-dotenv → to read API key from .env

from tools import calculator, get_country_info
from memory import load_memory, save_memory
from prompts import SYSTEM_PROMPT

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
print("DEBUG KEY =", OPENROUTER_API_KEY)

MODEL = "google/gemma-4-31b-it"   # you can change this

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# -----------------------------
# Tool schema shown to the LLM
# -----------------------------
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Perform basic arithmetic operations",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                    "operation": {
                        "type": "string",
                        "enum": ["add", "sub", "mul", "div"],
                        "description": "Arithmetic operation"
                    }
                },
                "required": ["a", "b", "operation"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_country_info",
            "description": "Fetch information about a country by its name",
            "parameters": {
                "type": "object",
                "properties": {
                    "country_name": {"type": "string", "description": "The name of the country (e.g. France, Japan)"}
                },
                "required": ["country_name"]
            }
        }
    }
]

# --------------------------------
# Map tool name to Python function
# --------------------------------
TOOL_FUNCTIONS = {
    "calculator": calculator,
    "get_country_info": get_country_info
}


def call_llm(messages):
    """
    Sends messages + tools to OpenRouter and returns the model response.
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "tools": TOOLS
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


def run_tool(tool_call):
    """
    Executes the tool requested by the model.
    """
    tool_name = tool_call["function"]["name"]
    tool_args = json.loads(tool_call["function"]["arguments"])

    if tool_name in TOOL_FUNCTIONS:
        result = TOOL_FUNCTIONS[tool_name](**tool_args)
        return str(result)
    else:
        return f"Error: Tool '{tool_name}' not found."


def agent_loop(user_input):
    """
    Core agent loop:
    1. Send user message to LLM
    2. If LLM asks for a tool -> run it
    3. Send tool result back to LLM
    4. Repeat until final answer
    """
    memory = load_memory()

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(memory)
    messages.append({"role": "user", "content": user_input})

    max_steps = 5

    for step in range(max_steps):
        result = call_llm(messages)
        message = result["choices"][0]["message"]

        # Save assistant response into conversation
        messages.append(message)

        # Check if model wants to call a tool
        if "tool_calls" in message and message["tool_calls"]:
            for tool_call in message["tool_calls"]:
                tool_result = run_tool(tool_call)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "name": tool_call["function"]["name"],
                    "content": tool_result
                })
        else:
            # Final answer from model
            final_answer = message.get("content", "No response generated.")
            
            # Save conversation to memory (excluding system prompt)
            save_memory(messages[1:])
            return final_answer

    return "Stopped: maximum tool loop steps reached."


if __name__ == "__main__":
    print("Beginner Agent is running. Type 'exit' to stop.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        try:
            answer = agent_loop(user_input)
            print("Agent:", answer)
        except Exception as e:
            print("Error:", e)