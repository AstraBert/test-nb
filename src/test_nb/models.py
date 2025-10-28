from typing import TypedDict, Any, Literal


class MarkdownCell(TypedDict):
    cell_type: Literal["markdown"]
    metadata: dict[str, Any]
    source: list[str]


class CodeCell(TypedDict):
    cell_type: Literal["code"]
    metadata: dict[str, Any]
    source: list[str]
    outputs: list[str]
    execution_count: int


class NotebookRunFailure(TypedDict):
    file: str
    return_code: int
    logs: str


class NotebookRunSuccess(TypedDict):
    file: str
    return_code: Literal[0]
    logs: str


class RunTestArgs(TypedDict):
    python_executable: str | None
    verbose: bool
    timeout: float | None
