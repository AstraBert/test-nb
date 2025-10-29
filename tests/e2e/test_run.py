import pytest
import os

from pathlib import Path
from test_nb.run import NotebookRunner


@pytest.fixture()
def runner() -> NotebookRunner:
    return NotebookRunner(
        directory="test_notebooks/",
    )


def test_convert_files_base(runner: NotebookRunner) -> None:
    assert all(
        el in runner.files
        for el in [
            "test_notebooks/normal.ipynb",
            "test_notebooks/with_bash.ipynb",
            "test_notebooks/with_env.ipynb",
        ]
    )
    try:
        runner.write_python_files(overwrite=True)
        success = True
    except Exception as e:
        success = False
    assert success
    assert len(runner._files_to_exec) == len(runner.files)
    for f in runner._files_to_exec:
        assert Path(f).exists() and Path(f).is_file()
        content = Path(f).read_text()
        try:
            assert (
                "import subprocess\nimport asyncio\n\nasync def main():\n\t" in content
            )
            assert "#" not in content
            if "normal.ipynb" in f:
                assert "subrpocess.run('pip install termcolor', shell=True)" in content
            elif "with_bash.ipynb" in f:
                assert (
                    "subrpocess.run('echo \\'hello world\\' && echo \\'this is a multiline bash\\'', shell=True)"
                    in content
                )
            elif "with_env.ipynb" in f:
                assert 'os.environ["SUPER_SECRET_KEY"] = "this is a key"' in content
        except AssertionError as e:
            raise e
        finally:
            os.remove(f)


def test_convert_files_markdown_as_comment(runner: NotebookRunner) -> None:
    runner.markdown_as_comment = True
    assert all(
        el in runner.files
        for el in [
            "test_notebooks/normal.ipynb",
            "test_notebooks/with_bash.ipynb",
            "test_notebooks/with_env.ipynb",
        ]
    )
    try:
        runner.write_python_files(overwrite=True)
        success = True
    except Exception as e:
        success = False
    assert success
    assert len(runner._files_to_exec) == len(runner.files)
    for f in runner._files_to_exec:
        assert Path(f).exists() and Path(f).is_file()
        content = Path(f).read_text()
        try:
            assert (
                "import subprocess\nimport asyncio\n\nasync def main():\n\t" in content
            )
            if "normal.ipynb" in f:
                assert (
                    "# This is _some_ **markdown** text which will be displayed as a `code comment`"
                    in content
                )
            elif "with_bash.ipynb" in f:
                assert "# Now we **execute** the function:" in content
            elif "with_env.ipynb" in f:
                assert "#" not in content
        except AssertionError as e:
            raise e
        finally:
            os.remove(f)


def test_convert_files_no_environ(runner: NotebookRunner) -> None:
    runner.exclude_env = True
    try:
        runner.write_python_files(overwrite=True)
        success = True
    except Exception as e:
        success = False
    assert success
    assert len(runner._files_to_exec) == len(runner.files)
    for f in runner._files_to_exec:
        assert Path(f).exists() and Path(f).is_file()
        content = Path(f).read_text()
        try:
            if "with_env.ipynb" in f:
                assert 'os.environ["SUPER_SECRET_KEY"] = "this is a key"' not in content
        except AssertionError as e:
            raise e
        finally:
            os.remove(f)


def test_convert_files_raise_on_error(runner: NotebookRunner) -> None:
    runner.exclude_env = True
    runner.write_python_files(overwrite=True)
    with pytest.raises(ValueError):
        runner.write_python_files()
    try:
        runner.write_python_files(raise_on_error=False)
        succ = True
    except Exception as e:
        succ = False
    assert succ
    for file in runner._files_to_exec:
        if Path(file).exists():
            os.remove(file)


def test_run_files(runner: NotebookRunner) -> None:
    runner.write_python_files(overwrite=True)
    try:
        passed, failed = runner.run(verbose=True)
    except Exception as e:
        passed, failed = [], ["Error"]
    assert len(failed) == 0
    assert len(passed) == 3
    for file in runner._files_to_exec:
        if Path(file).exists():
            os.remove(file)
