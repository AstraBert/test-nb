import os


def find_notebooks_in_dir(directory: str, recursive: bool):
    if recursive:
        files = []
        for root, _, filenames in os.walk(directory):
            for file in filenames:
                if file.endswith(".ipynb"):
                    files.append(os.path.join(root, file))
        return files
    else:
        return [
            os.path.join(directory, f)
            for f in os.listdir(directory)
            if os.path.join(directory, f).endswith(".ipynb")
        ]


def dir_exists(directory: str):
    return os.path.exists(directory) and os.path.isdir(directory)


def file_exists(file: str):
    return os.path.exists(file) and os.path.isfile(file)
