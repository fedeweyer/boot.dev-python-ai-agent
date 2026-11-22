import argparse
import json
import os
import sys
import time
from typing import Any, Dict, List

from dotenv import load_dotenv
from openai import OpenAI

from call_function import AVAILABLE_FUNCTIONS, call_function
from prompts import system_prompt
from rate_limiter import RateLimiter

MAX_ITERATIONS = 20


def get_env_var(var_name: str) -> str:
    """Retrieve an environment variable or raise RuntimeError if missing."""
    try:
        return os.environ[var_name]
    except KeyError:
        raise RuntimeError(f"{var_name} does not exist")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()


def create_client(api_key: str) -> OpenAI:
    """Create and configure the OpenAI client."""
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )


def build_messages(user_prompt: str) -> List[Dict[str, str]]:
    """Build the initial message list for the chat completion."""
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def get_usage(response: Any) -> Any:
    """Extract usage info from a response, raising if missing."""
    if response.usage is None:
        raise RuntimeError("usage info is missing from response")
    return response.usage


def handle_tool_calls(
    message: Any,
    messages: List[Dict[str, Any]],
    verbose: bool,
) -> None:
    """Process tool calls from the assistant message and append results."""
    for tool_call in message.tool_calls:
        function_args = json.loads(tool_call.function.arguments or "{}")
        result_message = call_function(tool_call, verbose)
        messages.append(result_message)

        if not result_message.get("content"):
            raise RuntimeError("no content")
        if verbose:
            print("-> Tool response:")
            print(f"{result_message['content']}")

def run_conversation(
    client: OpenAI,
    messages: List[Dict[str, Any]],
    verbose: bool,
    rate_limiter: RateLimiter,
    start_time: float,
) -> None:
    """Run the agent loop until a final answer is produced or max iterations reached."""
    for i in range(MAX_ITERATIONS):
        elapsed = time.time() - start_time

        print(f"Iteration {i}: Elapsed time since start: {elapsed:.2f} seconds")
        rate_limiter.wait_if_needed()
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            temperature=0,
            tools=AVAILABLE_FUNCTIONS,
        )

        usage = get_usage(response)

        if verbose:
            print(f"User prompt: {messages[-1]['content']}")
            print(f"Prompt tokens: {usage.prompt_tokens}")
            print(f"Response tokens: {usage.completion_tokens}")

        print("Response:")

        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls:
            handle_tool_calls(message, messages, verbose)
        else:
            print(message.content)
            sys.exit(0)

    sys.exit("max iterations exceeded")


def main() -> None:
    """Entry point for the chatbot application."""
    start_time = time.time()
    args = parse_args()
    load_dotenv()

    api_key = get_env_var("OPENROUTER_API_KEY")
    client = create_client(api_key)
    messages = build_messages(args.user_prompt)
    rate_limiter = RateLimiter(max_calls=5, period=60.0)

    run_conversation(client, messages, args.verbose, rate_limiter, start_time)


if __name__ == "__main__":
    main()
