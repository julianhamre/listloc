# listloc

`listloc`, short for **Listing Locator**, is a command-line interface (CLI) tool for extracting code listings from text-based source files. It scans a directory recursively and extracts all code blocks marked with `BEGIN LISTING <name>` and `END LISTING`. Each block is saved to its own `.listing` file inside a `listings/` directory.

---

## Purpose

`listloc` streamlines the process of managing code examples in documentation, especially LaTeX documents. Instead of copying and pasting code blocks or relying on line numbers when importing, you can declare listings directly in your source files and import the extracted `.listing` files. Automating the extraction process before each build or compile guarantees that your listings always reflect the latest source.

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

When extracted, a file named `greet.listing` is created in a `listings/` directory next to the source file. Every `.listing` file will contain the lines in between the listing declaration wrapper:

```text
def greet(name):
    print(f"Hello, {name}!")
```

Leading and trailing blank lines are removed from the extracted content.
For example, even this declaration:

```python
# BEGIN LISTING greet


def greet(name):
    print(f"Hello, {name}!")

# END LISTING
```

will result in the same extract:

```text
def greet(name):
    print(f"Hello, {name}!")
```
---

## CLI usage

The `--help` flag can also be used to view documentation.

### Extract Listings

```bash
listloc extract [--prune] [--verbose] [./path/to/project]
```

- Recursively scans UTF-8 source files in the given directory for listing declarations.
- Each listing is extracted to a `.listing` file inside a `listings/` directory located next to its source file.
- `--prune`: Deletes any stale `.listing` files that no longer match any listings in the source files.
- `--verbose`: Prints each file extracted from and every file or directory created or deleted.

### Clear Listings

```bash
listloc clear [--verbose] [./path/to/project]
```

- Recursively deletes all `.listing` files within the given directory.
- Removes any remaining `listings/` directories left empty after the `.listing` file deletions.
- `--verbose`: Prints every deleted file and directory.


If no directory path is provided for these commands, the current directory is used.

### Examples

- `listloc extract`
- `listloc clear --help`
- `listloc extract --prune --verbose my_project`

---

## Installation

### Option 1: Global installation

Install with pip
```bash
pip install git+https://github.com/julianhamre/listloc.git
```
This will make `listloc` available globally.

However, it’s recommended to install in a virtual environment to avoid conflicts with system packages.

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

Licensed under the [MIT License](/LICENSE.md).