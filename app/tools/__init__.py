from app.tools.bash import bash_schema, run_bash_command
from app.tools.read_file import read_file_schema, read_file
from app.tools.write_file import write_file_schema, write_file


TOOL_SCHEMAS = [
    bash_schema,
    read_file_schema,
    write_file_schema
]

TOOL_HANDLER = {
    "read_file": read_file,
    "write_file": write_file,
    "run_bash_command": run_bash_command,
}
