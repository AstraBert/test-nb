from test_nb.utils import find_notebooks_in_dir, file_exists, dir_exists


def test_file_exists() -> None:
    assert file_exists("README.md")
    assert not file_exists("READM.md")


def test_dir_exists() -> None:
    assert dir_exists("test_notebooks/")
    assert not dir_exists("tests_notebook/")


def test_find_notebooks_in_dir() -> None:
    notebooks = find_notebooks_in_dir("test_notebooks", False)
    assert all(
        el in notebooks
        for el in [
            "test_notebooks/normal.ipynb",
            "test_notebooks/with_bash.ipynb",
            "test_notebooks/with_env.ipynb",
        ]
    )
    notebooks = find_notebooks_in_dir("test_notebooks", True)
    assert all(
        el in notebooks
        for el in [
            "test_notebooks/normal.ipynb",
            "test_notebooks/with_bash.ipynb",
            "test_notebooks/with_env.ipynb",
            "test_notebooks/nested/notebook.ipynb",
        ]
    )
