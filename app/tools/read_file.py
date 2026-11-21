from app.tools.schema import ToolSchema, FunctionSchema, ParameterSchema


read_file_schema = ToolSchema(
    function=FunctionSchema(
        name="read_file",
        description="Read and return the contents of a file",
        parameters=ParameterSchema(
            type="object",
            properties={
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to read"
                }
            },
            required=["file_path"]
        ),
    ),
).model_dump()


def read_file(file_path: str) -> str:
    with open(file=file_path) as file:
        return file.read()
