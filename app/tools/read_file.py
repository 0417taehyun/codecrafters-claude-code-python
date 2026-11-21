from app.tools.schema import ToolSchema, FunctionSchema, ParameterSchema


read_file = ToolSchema(
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


if __name__ == "__main__":
    print(read_file)
