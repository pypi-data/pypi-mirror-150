# Raise Module Not Found Error

Raise Module Not Found Error is a "library" that raises a `ModuleNotFoundError` when an
attempt is made to import it.

## Example usage

```
>>> import raise_module_not_found_error
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "installation/path/raise_module_not_found_error.py", line 2, in <module>
    raise ModuleNotFoundError("Ceci n'est pas un module")
ModuleNotFoundError: Ceci n'est pas un module
```

## Running tests

Simply run `python -m unittest discover` in the project root.

## This is completely useless, isn't it?

yes
