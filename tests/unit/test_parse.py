import pytest

from test_nb.parse import extract_bash, extract_code
from test_nb.models import CodeCell


@pytest.fixture()
def code_cell_with_code() -> CodeCell:
    return {
        "cell_type": "code",
        "execution_count": 1,
        "metadata": {},
        "outputs": ["hello world!"],
        "source": [
            "def hello_world(name: str) -> None:",
            "\tprint(f'hello {name}!')",
            "hello_world('world')",
        ],
    }


@pytest.fixture()
def code_cell_with_code_environ() -> CodeCell:
    return {
        "cell_type": "code",
        "execution_count": 1,
        "metadata": {},
        "outputs": ["my-api-key"],
        "source": [
            "import os",
            "os.environ['X-API-KEY'] = 'my-api-key'",
            "print(os.getenv('X-API-KEY'))",
        ],
    }


@pytest.fixture()
def code_cell_with_code_and_bash() -> CodeCell:
    return {
        "cell_type": "code",
        "execution_count": 1,
        "metadata": {},
        "outputs": ["hello world!"],
        "source": [
            "!pip install termcolor",
            "%pip show termcolor",
            "from termcolor import cprint",
            "def hello_world_color(name: str, color: str) -> None:",
            "\tcprint(f'hello {name}!', color=color)",
            "hello_world_color('world', 'red)",
        ],
    }


@pytest.fixture()
def code_cell_with_bash() -> CodeCell:
    return {
        "cell_type": "code",
        "execution_count": 1,
        "metadata": {},
        "outputs": ["hey there", "how are you?"],
        "source": ["%%bash", "echo 'hey there'", "echo 'how are you?'"],
    }


def test_parsing_utils_with_code_only(code_cell_with_code: CodeCell) -> None:
    code = extract_code(code_cell_with_code)
    bash = extract_bash(code_cell_with_code)
    assert bash is None
    assert code is not None
    for item in code_cell_with_code["source"]:
        assert "\t" + item in code


def test_parsing_utils_with_code_environ(code_cell_with_code_environ: CodeCell) -> None:
    code = extract_code(code_cell_with_code_environ)
    assert code is not None
    assert "os.environ['X-API-KEY'] = 'my-api-key'" in code
    code = extract_code(code_cell_with_code_environ, exclude_env=True)
    assert code is not None
    assert "os.environ['X-API-KEY'] = 'my-api-key'" not in code


def test_parsing_utils_with_bash_only(code_cell_with_bash: CodeCell) -> None:
    code = extract_code(code_cell_with_bash)
    bash = extract_bash(code_cell_with_bash)
    assert code is None
    assert bash is not None
    assert bash == "echo 'hey there' && echo 'how are you?'"


def test_parsing_utils_with_code_and_bash(
    code_cell_with_code_and_bash: CodeCell,
) -> None:
    code = extract_code(code_cell_with_code_and_bash)
    bash = extract_bash(code_cell_with_code_and_bash)
    assert code is not None
    assert bash is not None
    assert bash == "pip install termcolor && pip show termcolor"
    for item in code_cell_with_code_and_bash["source"]:
        if not item.startswith("!") and not item.startswith("%"):
            assert "\t" + item in code
