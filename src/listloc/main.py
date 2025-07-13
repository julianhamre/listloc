import typer
from typing_extensions import Annotated
import os
from extractor.listing_extractor import ListingExtractor


app = typer.Typer()

@app.command()
def extract(path: Annotated[str, typer.Argument()] = os.getcwd()):
    """
    Extract all listings from the files under the given directory. If no path is provided, the current working directory is used.
    """
    extractor = ListingExtractor(path)
    extractor.extract_all_listings()
    typer.echo(f"Extracted listings from {path}")

@app.command()
def clear(path: Annotated[str, typer.Argument()] = os.getcwd()):
    """
    Delete all extracted listing files under the given directory. Every listing directory only containing extracted listings will be deleted as well. If no path is provided, the current working directory is used.
    """
    extractor = ListingExtractor(path)
    extractor.clear_all_listing_extractions()
    typer.echo(f"Cleared listings from {path}")


if __name__ == "__main__":
    app()