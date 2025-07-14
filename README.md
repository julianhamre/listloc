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

## CLI usage

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

### Option 1: Global installation

Install with pip
```bash
pip install git+https://github.com/julianhamre/listloc.git
```
This will make `listloc` available globally.

It’s recommended to install in a virtual environment to avoid conflicts with system packages.

### Option 2: Install for development

First, clone the repository

```bash
git clone https://github.com/julianhamre/listloc.git
cd listloc
```

Install with [Poetry](https://python-poetry.org/).

```bash
poetry install
```
This installs `listloc` in a virtual environment managed by Poetry.

Thereafter, run
```bash
poetry env activate
```
This will print the source command that can activate the virtual environment. Activate it manually by running that source command.

Finally, run
```bash
listloc --help
```
to ensure that `listloc` was successfully installed.

---


## License

Licensed under the [MIT License](https://mit-license.org).