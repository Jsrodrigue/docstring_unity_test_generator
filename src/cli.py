import typer
from src.core.docstring_scanner import scan_folder_for_docstrings

# Create a Typer app instance
# This is the main entry point for the CLI
app = typer.Typer(help="Python docstring scanner and updater")

# Define a CLI command using the @app.command() decorator
@app.command()
def scan(
    # Define a required positional argument 'path'
    path: str = typer.Argument(
        ...,    # '...' means this argument is required
        help="Folder to scan for Python files"  # Help text for this argument
    ), 
    # Define an optional option 'mode' with default value 'review'
    mode: str = typer.Option(
        "review",  # Default value
        "--mode",  # Long option name
        "-m",      # Short option name
        help="Mode: 'review' asks for confirmation, 'auto' updates automatically"
    )
):
    """
    Scan a folder recursively for Python files and generate/improve docstrings.
    
    This docstring will appear in CLI help automatically.
    """
    # Call the main scanning function with the provided arguments
    scan_folder_for_docstrings(path, mode)

if __name__ == "__main__":
    app()
