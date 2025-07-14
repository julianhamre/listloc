# listloc

`listloc`, short for **Listing Locator**, is a command-line interface (CLI) tool for extracting code listings from text-based source files. It scans a directory recursively and extracts all code blocks marked with `BEGIN LISTING <name>` and `END LISTING`. Each block is saved to its own `.listing` file inside a `listings/` directory.

---

## How to declare Listings

To mark a code listing for extraction in a source file, wrap it between a `BEGIN LISTING <listing_name>` and `END LISTING` comment.

Example:
```python
# BEGIN LISTING greet
def greet(name):
    print(f"Hello, {name}!")
# END LISTING
```

If extracted, a file called `greet.listing` will be created and saved in a `listings/` directory in the same location as the source file. Every `.listing` file will contain the content in between the listing declaration wrapper:

```text
def greet(name):
    print(f"Hello, {name}!")
```

---


### Extract Listings

```bash
listloc extract ./path/to/project
```

- Recursively scans for listing declarations.
- Outputs extracted listings to `listings/` directories.

### Clear Listings

```bash
listloc clear ./path/to/project
```

- Recursively deletes all `.listing` files within the given directory.
- Removes any `listings/` directories only containing `.listing` files.


If no path is provided for these commands, the current directory is used.

---

## Installation

```bash
git clone https://github.com/julianhamre/listloc.git
cd path/to/listloc
```

Then install with [Poetry](https://python-poetry.org/)

### Alternative 1: System-wide installation

```bash
poetry build
pip install ./dist/listloc-<VERSION>-py3-none-any.whl
```

### Alternative 2: For development

Create and activate a virtual environment and run
```bash
poetry install
```

After any successful install you will be able to run

```bash
listloc --help
```
---


## License

Licensed under the [MIT License](https://mit-license.org).