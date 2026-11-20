import os
from dotenv import load_dotenv
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function
import json

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

args = parser.parse_args()

load_dotenv()

def get_my_env_var(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        raise RuntimeError(f"{var_name} does not exist")



api_key = get_my_env_var("OPENROUTER_API_KEY")

from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    temperature=0,
    tools=available_functions,
)

def get_usage(response):
    if response.usage is None:
        raise RuntimeError(f"{var_name} does not exist")
    return response.usage


usage = get_usage(response)

if args.verbose is True:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {usage.prompt_tokens}")
    print(f"Response tokens: {usage.completion_tokens}")
print("Response:")

message = response.choices[0].message

if message.tool_calls:
    for tool_call in message.tool_calls:
        function_args = json.loads(tool_call.function.arguments or "{}")
        print(f"Calling function: {tool_call.function.name}({function_args})")
        result_message = call_function(tool_call, args.verbose)

        if not result_message.get("content"):
            raise RuntimeError("no content")
        if args.verbose:
            print(f"-> {result_message['content']}")
else:
    message = message.content
print(message)


