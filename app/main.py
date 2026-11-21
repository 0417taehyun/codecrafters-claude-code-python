import argparse
import os
import json

from openai import OpenAI

from app.tools import TOOL_HANDLER, read_file_schema


API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")
MAXIMUM_STEPS = os.getenv("MAXIMUM_STEPS", default=10)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    steps = 1
    messages = [{"role": "user", "content": args.p}]
    while steps <= MAXIMUM_STEPS:
        response = client.chat.completions.create(
            model="anthropic/claude-haiku-4.5",
            messages=messages,
            tools=[read_file_schema]
        )

        if not response.choices or len(response.choices) == 0:
            raise RuntimeError("no choices in response")

        message = response.choices[0].message
        messages.append(message)
        
        if not message.tool_calls:
            print(message.content)
            break

        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            handler = TOOL_HANDLER.get(function_name)
            if handler:
                result = handler(**arguments)
            else:
                result = f"Error: unknown tool: {function_name}"

            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})

        steps += 1


if __name__ == "__main__":
    main()
