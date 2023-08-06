# librep - LIne Block REPlacement

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI version](https://badge.fury.io/py/librep.svg)](https://badge.fury.io/py/librep)

![Testing workflow](https://github.com/umami-hep/librep/actions/workflows/testing.yml/badge.svg)
![Linting workflow](https://github.com/umami-hep/librep/actions/workflows/linting.yml/badge.svg)

`librep` is a python-based command-line tools allows to render file placeholders.
It replaces a placeholder of a given syntax with the content of the file that is
specified in the placeholder.

The tool is independent of the document type, since it is assumed that the chosen
syntax does not interfere with the syntax of any (especially markup) language.

The indentation of the placeholder is used for the whole inserted code/text block.

## Usage

Insert a placeholder of the following syntax inside a file:

```md
§§§<filename>:<start>:<end>§§§
```

Afterwards, you can render the placeholder by running

```bash
$ librep -i "file_with_placeholder.md"
```

This will replace the original line in the file `file_with_placeholder.md` with
the content of the file `<filename>` from line `<start>` to line `<end>`.
The `filename` has to either be absolute or relative to the file you specify the
placeholder in.

**Using a URL instead of a file from the repository**

If you want to link a file that is not present on your machine, but you have a URL
to that exact file, you can use the following syntax:

```md
§§§url="<url>":<start>:<end>§§§
```

_Note that this requires `wget` to be installed on your machine_

## Example

This file `file_with_placeholders.md`

````md
# Heading

Check out this awesome python code!

```py
§§§./code.py§§§
```
````

Can be processed with `librep` by doing

```bash
$ librep -i "file_with_placeholder.md"
```

Which results in

````md
# Heading

Check out this awesome python code!

```py
def calc_sum(a, b):
    """Calculates the sum of a+b
    Parameters
    ----------
    a : float, int
        First number
    b : float, int
        Second number
    Returns
    -------
    sum : float
        Sum of a and b
    """

    return a + b
```
````

## Examples

Below you can find different versions for inserting different parts of the file
`examples/plotting/plot_rocs.py` into your markdown file.

| Placeholder                    | Result                  |
| ------------------------------ | ----------------------- |
| `§§§examples/file.py§§§`       | whole file              |
| `§§§examples/file.py::§§§`     | whole file              |
| `§§§examples/file.py:10:20§§§` | from line 10 to line 20 |
| `§§§examples/file.py::10§§§`   | from top to line 10     |
| `§§§examples/file.py:10§§§`    | from line 10 to bottom  |
| `§§§examples/file.py:10:§§§`   | from line 10 to bottom  |

## Installation

`librep` can simply be installed using `pip install`:

```bash
pip install librep
# or
pip install https://github.com/umami-hep/librep/archive/master.tar.gz
```
