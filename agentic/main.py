import os
from dotenv import load_dotenv
import argparse
from prompts import system_prompt

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
print(response.choices[0].message.content)

