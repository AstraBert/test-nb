import pytest
import os

from pathlib import Path
from test_nb.cli.commands import _convert_files_and_run_if_needed
from test_nb.utils import find_notebooks_in_dir


@pytest.fixture()
def notebooks() -> tuple[str, ...]:
    return tuple(find_notebooks_in_dir("test_notebooks/", False))


def test_cli_convert(notebooks: tuple[str, ...]):
    _convert_files_and_run_if_needed(
        file=notebooks,
        overwrite=True,
    )
    for file in notebooks:
        assert (
            Path(file.replace(".ipynb", ".py")).exists()
            and Path(file.replace(".ipynb", ".py")).is_file()
        )
        os.remove(file.replace(".ipynb", ".py"))


def test_cli_run_tests(notebooks: tuple[str, ...]):
    try:
        _convert_files_and_run_if_needed(
            file=notebooks,
            overwrite=True,
            run_test_args={"python_executable": None, "timeout": None, "verbose": True},
        )
        succ = True
    except Exception as e:
        succ = False
    assert succ
    for file in notebooks:
        assert (
            Path(file.replace(".ipynb", ".py")).exists()
            and Path(file.replace(".ipynb", ".py")).is_file()
        )
        os.remove(file.replace(".ipynb", ".py"))
