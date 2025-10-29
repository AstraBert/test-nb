import json
import sys
import subprocess

from termcolor import cprint
from .models import CodeCell, MarkdownCell, NotebookRunFailure, NotebookRunSuccess
from .utils import find_notebooks_in_dir, file_exists, dir_exists
from .parse import extract_bash, extract_code


class NotebookRunner:
    def __init__(
        self,
        file_paths: list[str] | None = None,
        directory: str | None = None,
        recursive: bool = False,
        markdown_as_comment: bool = False,
        exclude_env: bool = False,
    ):
        if not file_paths and not directory:
            raise ValueError(
                "At least one of `file_paths` and `directoray` should be provided"
            )
        self._files_to_exec: list[str] = []
        self.files: list[str] = []
        if file_paths is not None:
            if len(file_paths) == 0:
                raise ValueError("Cannot pass an empty list as `file_paths` parameter")
            for file in file_paths:
                if file_exists(file):
                    self.files.append(file)
                else:
                    print(
                        f"File {file} does not exist or it is not a file, skipping...",
                        file=sys.stderr,
                    )
            if len(self.files) == 0:
                raise ValueError("None of the provided files exists")
        if directory is not None:
            if dir_exists(directory):
                _snapshot_len = len(self.files)
                self.files.extend(find_notebooks_in_dir(directory, recursive))
                if _snapshot_len == len(self.files) and len(self.files):
                    raise ValueError(
                        f"Directory {directory} did not contain any .ipynb file"
                        + " even if `recursive` is set to True"
                        if recursive
                        else ". Try setting `recursive` to True."
                    )
            else:
                raise ValueError(
                    f"Directory {directory} does not exist or is not a directory"
                )
        self.markdown_as_comment = markdown_as_comment
        self.exclude_env = exclude_env

    def write_python_files(self, raise_on_error: bool = True, overwrite: bool = False):
        for file in self.files:
            with open(file, "r") as f:
                data = json.load(f)
            if "cells" not in data:
                msg = f"File {file} does not have any cells, please exclude it from the files to process and re-try"
                if raise_on_error:
                    raise ValueError(msg)
                else:
                    print(msg.split(",")[0], file=sys.stderr)
                    continue
            cells: list[MarkdownCell | CodeCell] = data["cells"]
            script = "import subprocess\nimport asyncio\n\nasync def main():\n"
            for cell in cells:
                if cell["cell_type"] == "markdown" and self.markdown_as_comment:
                    for line in cell["source"]:
                        if line.strip():
                            script += "\t# " + line + "\n"
                elif cell["cell_type"] == "code":
                    bash = extract_bash(cell)
                    if bash:
                        sanitized_bash = bash.strip().replace("'", "\\'")
                        script += f"\tsubprocess.run('{sanitized_bash}', shell=True)\n"
                    code = extract_code(cell, self.exclude_env)
                    if code:
                        script += f"{code}\n"
            script += "\n\nasyncio.run(main())"
            py_file_name = file.replace(".ipynb", ".py")
            if file_exists(py_file_name) and not overwrite:
                msg = f"Python file {py_file_name} already exist and permission to overwrite has not been granted"
                if raise_on_error:
                    raise ValueError(msg)
                else:
                    print(msg + ". Skipping...", file=sys.stderr)
                    continue
            else:
                with open(py_file_name, "w") as f:
                    f.write(script)
                self._files_to_exec.append(py_file_name)

    def run(
        self,
        python_executable: str | None = None,
        timeout: float | None = None,
        verbose: bool = False,
    ) -> tuple[list[NotebookRunSuccess], list[NotebookRunFailure]]:
        succ: list[NotebookRunSuccess] = []
        fail: list[NotebookRunFailure] = []
        if len(self._files_to_exec) == 0:
            raise ValueError(
                "No files to execute, please convert some files before using this method"
            )
        if not python_executable:
            python_executable = sys.executable
        for file in self._files_to_exec:
            result = subprocess.run(
                python_executable + " " + file,
                shell=True,
                capture_output=True,
                timeout=timeout,
            )
            if result.returncode != 0:
                fail.append(
                    {
                        "return_code": result.returncode,
                        "logs": str(result.stderr, encoding="utf-8"),
                        "file": file,
                    }
                )
                cprint(f"{file} FAILED", color="red", attrs=["bold"])
            else:
                succ.append(
                    {
                        "return_code": result.returncode,  # type: ignore
                        "logs": str(result.stdout, encoding="utf-8"),
                        "file": file,
                    }
                )
                cprint(f"{file} PASSED", color="green", attrs=["bold"])
        print()
        print()
        print("=========== TEST SUMMARY =============")
        print()
        cprint(f"{len(succ)} tests were successfull", color="green", attrs=["bold"])
        cprint(f"{len(fail)} tests failed\n", color="red", attrs=["bold"])
        if len(fail) > 0:
            for f in fail:
                print(f"\t- {f['file']}\n")
                if verbose:
                    print(f"\t\tReturn Code: {f['return_code']}\n")
                    print(f"\t\tCaptured Logs: {f['logs']}\n\n")
            if not verbose:
                cprint(
                    f"\t\t(enable the `--verbose` option to see details)",
                    color="yellow",
                    attrs=["bold"],
                )
        return succ, fail
