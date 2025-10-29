# test-nb

Custom utilities to convert notebooks to python and test them.

## CLI Reference

```text
Usage: nb [OPTIONS] COMMAND [ARGS]

  Convert notebooks to python scripts and run them for testing purposes

Options:
  --help  Show this message and exit.

Commands:
  convert  Convert notebook to python files
  test     Convert notebook to python files and test them end-to-end by running them
```

## Commands

**convert**

```text
Usage: nb convert [OPTIONS]

  Convert notebooks to python files

Options:
  --file TEXT       Include one or more notebook files to convert to python
  --directory TEXT  Directory from which to convert notebooks.
  --recursive       Search recursively for notebooks in the provided directory
  --include-md      Include markdown (as comments) in the script
  --no-errors       Silence errors when reading from notebooks and writing to
                    python files.
  --exclude-env     Exclude code that sets environment variables
                    (os.environ[*] = *)
  --overwrite       Overwrite existing files when converting to python.
  --help            Show this message and exit.
```

**test**

```text
Usage: nb test [OPTIONS]

  Convert notebook to python files and test them end-to-end by running them

Options:
  --file TEXT               Include one or more notebook files to convert to
                            python
  --directory TEXT          Directory from which to convert notebooks.
  --recursive               Search recursively for notebooks in the provided
                            directory
  --include-md              Include markdown (as comments) in the script
  --no-errors               Silence errors when reading from notebooks and
                            writing to python files.
  --exclude-env             Exclude code that sets environment variables
                            (os.environ[*] = *)
  --overwrite               Overwrite existing files when converting to
                            python.
  --python-executable TEXT  Path to the python executable. Defaults to
                            executable in the current environment if not
                            provided
  --verbose                 Verbose logging for tests.
  --timeout FLOAT           Timeout for notebook execution
  --help                    Show this message and exit.
```
