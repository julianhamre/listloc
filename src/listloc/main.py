import typer
from typing_extensions import Annotated
from rich.markdown import Markdown
import os
from listloc.extractor.listing_extractor import ListingExtractor


app = typer.Typer(rich_markup_mode="rich", help="""
Extract and manage code listings from source files.

See: https://github.com/julianhamre/listloc for more examples and usage.
""")

@app.command()
def extract(
    path: Annotated[str, typer.Argument()] = os.getcwd(),
    prune: Annotated[bool, typer.Option(
        help="Delete any extracted .listing files that no longer correspond to a declared listing in the source files.")] = False):
    """
    Recursively extract all declared code listings from UTF-8 encoded source files under the given directory.

    Each code listing is the content between `BEGIN LISTING <listing_name>` and `END LISTING`.
    Extracted listings are saved as `.listing` files inside `listings/` directories.

    If no directory path is provided, the current working directory is used.

    Example: listloc extract ./my_project
    """
    extractor = ListingExtractor(path)
    if prune:
        clear(path)
    any_listing_extracted = extractor.extract_all_listings()
    if any_listing_extracted:
        typer.echo(f"Extracted listings from {path}")
    else:
        typer.echo(f"No listings to extract from {path}")

@app.command()
def clear(path: Annotated[str, typer.Argument()] = os.getcwd()):
    """
    Recursively delete all extracted `.listing` files under the given directory.

    Any `listings/` directory that contains only `.listing` files will also be deleted.

    If no path is provided, the current working directory is used.

    Example: listloc clear ./my_project
    """
    extractor = ListingExtractor(path)
    any_listing_files_or_dirs_deleted = extractor.clear_all_listing_extractions()
    if any_listing_files_or_dirs_deleted:
        typer.echo(f"Deleted listings in {path}")
    else:
        typer.echo(f"No listing files or directories to delete in {path}")


if __name__ == "__main__":
    app()