import click
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def _file_option(f: Callable[P, R]) -> Callable[P, R]:
    return click.option(
        "--file",
        help="Include one or more notebook files to convert to python",
        multiple=True,
        required=False,
        default=None,
    )(f)


def _directory_option(f: Callable[P, R]) -> Callable[P, R]:
    return click.option(
        "--directory",
        help="Directory from which to convert notebooks.",
        required=False,
        default=None,
    )(f)


def _recursive_option(f: Callable[P, R]) -> Callable[P, R]:
    return click.option(
        "--recursive",
        help="Search recursively for notebooks in the provided directory",
        is_flag=True,
        required=False,
        default=False,
    )(f)


def _include_md_option(f: Callable[P, R]) -> Callable[P, R]:
    return click.option(
        "--include-md",
        help="Include markdown (as comments) in the script",
        is_flag=True,
        required=False,
        default=False,
    )(f)


def _overwrite_option(f: Callable[P, R]) -> Callable[P, R]:
    return click.option(
        "--overwrite",
        help="Overwrite existing files when converting to python.",
        is_flag=True,
        required=False,
        default=False,
    )(f)


def _no_errors_option(f: Callable[P, R]) -> Callable[P, R]:
    return click.option(
        "--no-errors",
        help="Silence errors when reading from notebooks and writing to python files.",
        is_flag=True,
        required=False,
        default=False,
    )(f)


def _exclude_env_option(f: Callable[P, R]) -> Callable[P, R]:
    return click.option(
        "--exclude-env",
        help="Exclude code that sets environment variables (os.environ[*] = *)",
        is_flag=True,
        required=False,
        default=False,
    )(f)


def common_options(f: Callable[P, R]) -> Callable[P, R]:
    return _file_option(
        _directory_option(
            _recursive_option(
                _include_md_option(
                    _no_errors_option(_exclude_env_option(_overwrite_option(f)))
                )
            )
        )
    )
