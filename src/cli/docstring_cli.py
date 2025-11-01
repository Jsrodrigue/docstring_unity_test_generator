import typer
from src.docstring_core.docstring_scanner import scan_folder_for_docstrings
from constants import models
app = typer.Typer(help="Python docstring auto-generator and updater")


@app.command()
def scan_and_generate(
    path: str = typer.Argument(
        ...,
        help="Path to file or folder to scan for Python files"
    ),
    model_name: str = typer.Option(
        "gpt-4o-mini",
        "--model",
        "-m",
        help=(
            "Model to use for generating docstrings "
            f"(available: {', '.join(models)}; default: gpt-4o-mini)"
        ),
        case_sensitive=False,
    ),
):
    """
    Automatically scan a folder or file and update docstrings using the selected model.
    """
    if model_name not in models:
        typer.echo(f"❌ Invalid model '{model_name}'. Available options:\n{', '.join(models)}")
        raise typer.Exit(code=1)

    scan_folder_for_docstrings(path, model_name=model_name)


if __name__ == "__main__":
    app()
