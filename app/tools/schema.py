from typing import Any, Literal

from pydantic import BaseModel


class ToolSchema(BaseModel):
    type: Literal["function"] = "function"
    function: FunctionSchema


class FunctionSchema(BaseModel):
    name: str
    description: str
    parameters: ParameterSchema


class ParameterSchema(BaseModel):
    type: str | None
    properties: dict[str, Any]
    required: list[str]

