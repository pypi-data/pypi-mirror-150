# librep

librep - LIne Block REPlacement

This python-based command-line tools allows to render file placeholders in other files.
The tools is independent of the document type, since it is assumed that the chosen
syntax does not interfere with syntax of any (especially markup) languages.
The indent of the placeholder is used for the whole inserted code/text block.

## Usage

Insert a placeholder of the following syntax inside a file (here 
`file_with_placeholder.md`):

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

*Note that this requires `wget` to be installed on your machine*


## Examples

Below you can find different versions for inserting different parts of the file 
`examples/plotting/plot_rocs.py` into your markdown file.

| Placeholder | Result |
|-------------|--------|
|`§§§examples/file.py§§§` | whole file |
|`§§§examples/file.py::§§§` | whole file |
|`§§§examples/file.py:10:20§§§` | from line 10 to line 20 |
|`§§§examples/file.py::10§§§` | from top to line 10 |
|`§§§examples/file.py:10§§§` | from line 10 to bottom |
|`§§§examples/file.py:10:§§§` | from line 10 to bottom |

## Installation

`librep` can simply be installed using `pip install`:

```bash
pip install librep
# or
pip install https://github.com/umami-hep/librep/archive/master.tar.gz