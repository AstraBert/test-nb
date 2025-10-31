import click
import sys

from .app import app
from .options import common_options
from test_nb.run import NotebookRunner
from test_nb.models import RunTestArgs


@app.command(
    "convert",
    help="Convert notebook to python files",
)
@common_options
def convert(
    file: tuple[str, ...] | None = None,
    directory: str | None = None,
    recursive: bool = False,
    include_md: bool = False,
    overwrite: bool = False,
    no_errors: bool = False,
    exclude_env: bool = False,
) -> None:
    retcode = _convert_files_and_run_if_needed(
        file=file,
        directory=directory,
        recursive=recursive,
        overwrite=overwrite,
        include_md=include_md,
        no_errors=no_errors,
        exclude_env=exclude_env,
    )
    sys.exit(retcode)


@app.command(
    "test",
    help="Convert notebook to python files and test them end-to-end by running them",
)
@common_options
@click.option(
    "--python-executable",
    help="Path to the python executable. Defaults to executable in the current environment if not provided",
    required=False,
    default=None,
)
@click.option(
    "--verbose",
    help="Verbose logging for tests.",
    required=False,
    default=False,
    is_flag=True,
)
@click.option(
    "--timeout",
    help="Timeout for notebook execution",
    type=float,
    required=False,
    default=None,
)
def test(
    file: tuple[str, ...] | None = None,
    directory: str | None = None,
    recursive: bool = False,
    include_md: bool = False,
    overwrite: bool = False,
    no_errors: bool = False,
    exclude_env: bool = False,
    python_executable: str | None = None,
    verbose: bool = False,
    timeout: float | None = None,
) -> None:
    retcode = _convert_files_and_run_if_needed(
        file=file,
        directory=directory,
        recursive=recursive,
        overwrite=overwrite,
        include_md=include_md,
        no_errors=no_errors,
        exclude_env=exclude_env,
        run_test_args={
            "python_executable": python_executable,
            "timeout": timeout,
            "verbose": verbose,
        },
    )
    sys.exit(retcode)


def _convert_files_and_run_if_needed(
    file: tuple[str, ...] | None = None,
    directory: str | None = None,
    recursive: bool = False,
    include_md: bool = False,
    overwrite: bool = False,
    no_errors: bool = False,
    exclude_env: bool = False,
    run_test_args: RunTestArgs | None = None,
) -> int:
    files: list[str] | None = None
    if file is not None and len(file) > 0:
        files = list(file)
    try:
        runn = NotebookRunner(
            file_paths=files,
            directory=directory,
            recursive=recursive,
            markdown_as_comment=include_md,
            exclude_env=exclude_env,
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        raise click.Abort()

    try:
        runn.write_python_files(no_errors, overwrite)
    except Exception as e:
        return 1

    if run_test_args is not None:
        _, fail = runn.run(
            python_executable=run_test_args["python_executable"],
            timeout=run_test_args["timeout"],
            verbose=run_test_args["verbose"],
        )
        return 1 if len(fail) > 0 else 0

    return 0
