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
def extract(path: Annotated[str, typer.Argument()] = os.getcwd()):
    """
    Recursively extract all declared code listings from the source files under the given directory.

    Each code listing is the content between `BEGIN LISTING <listing_name>` and `END LISTING`.
    Extracted listings are saved as `.listing` files inside `listings/` directories.

    If no directory path is provided, the current working directory is used.

    Example: listloc extract ./my_project
    """
    extractor = ListingExtractor(path)
    extractor.extract_all_listings()
    typer.echo(f"Extracted listings from {path}")

@app.command()
def clear(path: Annotated[str, typer.Argument()] = os.getcwd()):
    """
    Recursively delete all extracted `.listing` files under the given directory.

    Any `listings/` directory that contains only `.listing` files will also be deleted.

    If no path is provided, the current working directory is used.

    Example: listloc clear ./my_project
    """
    extractor = ListingExtractor(path)
    extractor.clear_all_listing_extractions()
    typer.echo(f"Cleared listings from {path}")


if __name__ == "__main__":
    app()