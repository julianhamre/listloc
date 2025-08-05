import typer
from typing_extensions import Annotated
from importlib.metadata import version, PackageNotFoundError
from rich import print
import os
from listloc.extractor.listing_extractor import ListingExtractor
from listloc.extractor.action_logger import ActionLogger
from listloc.extractor.listing import ListingError


app = typer.Typer(
    rich_markup_mode="rich",
    help="""Extract and manage code listings declared in text-based source files.""",
)

def get_version_from_metadata():
    try:
        return version("listloc")
    except PackageNotFoundError:
        return "unknown"

def version_callback(value: bool):
    if value:
        typer.echo(get_version_from_metadata())
        raise typer.Exit()

@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Show the version and exit."
        )] = False
        ):
    pass


def run_and_hide_exception_traceback(command_runner, *args):
    try:
        command_runner(*args)
    except (ListingError, NotADirectoryError, FileNotFoundError, PermissionError, UnicodeDecodeError) as e:
        print(f"[bold red]Error:[/bold red] {e}")
    except Exception as e:
        print(f"[bold red]Unexpected error:[/bold red] {e}")
    raise typer.Exit(1)

def create_extractor(path: str, verbose: bool):
    logger = ActionLogger(path, verbose=verbose)
    return ListingExtractor(path, logger), logger

def run_extract(path: str, verbose: bool, prune: bool):
    extractor, logger = create_extractor(path, verbose)
    if prune:
        extractor.clear_all_listing_extractions()
    extractor.extract_all_listings()
    logger.summarize_or_note_no_extractions()

@app.command()
def extract(
    path: Annotated[str, typer.Argument()] = os.getcwd(),
    verbose: Annotated[bool, typer.Option(
        help="Print each file extracted from and every file or directory created or deleted.")] = False,
    prune: Annotated[bool, typer.Option(
        help="Delete any extracted [bold].listing[/bold] files that no longer correspond to a declared listing in the source files.")] = False,
    ):
    """
    Recursively extract all declared code listings from UTF-8 encoded source files under the given directory.

    Each code listing includes the lines between [cyan]BEGIN LISTING <listing_name>[/cyan] and [cyan]END LISTING[/cyan], with any leading or trailing blank lines automatically removed. Extracted listings are saved as [bold].listing[/bold] files inside [bold]listings/[/bold] directories.

    If no directory path is provided, the current working directory is used.

    Example: 
        listloc extract ./my_project
    """
    run_and_hide_exception_traceback(run_extract, path, verbose, prune)


def run_clear(path: str, verbose: bool):
    extractor, logger = create_extractor(path, verbose)
    extractor.clear_all_listing_extractions()
    logger.summarize_or_note_no_clearings()

@app.command()
def clear(path: Annotated[str, typer.Argument()] = os.getcwd(),
          verbose: Annotated[bool, typer.Option(
              help="Print every deleted file and directory")] = False):
    """
    Recursively delete all extracted [bold].listing[/bold] files under the given directory.

    Every [bold]listings/[/bold] directory left empty after the deletions will also be removed.

    If no path is provided, the current working directory is used.

    Example: 
        listloc clear ./my_project
    """
    run_and_hide_exception_traceback(run_clear, path, verbose)


if __name__ == "__main__":
    app()