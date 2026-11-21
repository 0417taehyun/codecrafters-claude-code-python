from app.tools.schema import ToolSchema, FunctionSchema, ParameterSchema


write_file_schema = ToolSchema(
    function=FunctionSchema(
        name="write_file",
        description="Write content to a file",
        parameters=ParameterSchema(
            type="object",
            properties={
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to write to"
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file"
                }
            },
            required=["file_path", "content"]
        )
    )
).model_dump()


def write_file(file_path: str, content: str) -> str:
    with open(file=file_path, mode="w") as file:
        file.write(content)
    return f"Finished to write content to {file_path}"
