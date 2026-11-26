import argparse
import os
import sys
import json

from pathlib import Path

from openai import OpenAI

from app.tools import TOOL_SCHEMAS, TOOL_HANDLER
from app.utils import SkillParser


API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")
MAXIMUM_STEPS = int(os.getenv("MAXIMUM_STEPS", default="10"))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    parser = SkillParser()
    skills = [
        skill.model_dump() for skill
        in parser.read_skills(paths=sorted(Path(__file__).resolve().parent.rglob("*/SKILL.md")))
    ]

    step = 1
    messages = [
        {
            "role": "system",
            "content": (
                f"You are a coding agent working in {os.getcwd()}. "
                "Use the tools to complete the user's requests."
                "Also, You have access to the following skills with format {\"name\": ..., \"description\": ...}:\n"
                f"{json.dumps(skills)}"
            )
        },
        {"role": "user", "content": args.p},
    ]

    print("message: ", messages)

    while step <= MAXIMUM_STEPS:
        response = client.chat.completions.create(
            model="anthropic/claude-haiku-4.5",
            messages=messages,
            tools=TOOL_SCHEMAS
        )

        if not response.choices or len(response.choices) == 0:
            raise RuntimeError("no choices in response")

        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            print(f"[step {step}] no tool call", file=sys.stderr)
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

            print(f"[step {step}] {function_name}({arguments}) -> {result!r}", file=sys.stderr)
            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})

        step += 1


if __name__ == "__main__":
    main()
