import subprocess

from app.tools.schema import ToolSchema, FunctionSchema, ParameterSchema


bash_schema = ToolSchema(
    function=FunctionSchema(
        name="run_bash_command",
        description="Execute a shell command",
        parameters=ParameterSchema(
            type="object",
            properties={
                "command": {
                    "type": "string",
                    "description": "The command to execute"
                }
            },
            required=["command"]
        )
    )
).model_dump()


def run_bash_command(command: str) -> str:
    response = subprocess.run(command, shell=True,
                              capture_output=True, text=True)

    if response.returncode != 0:
        return response.stderr

    return response.stdout

