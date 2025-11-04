import typer
from src.docstring_core.docstring_executor import execute_docstring_in_path
from constants import models

docstring_app = typer.Typer(help="Python docstring auto-generator and updater")

@docstring_app.command()
def scan_and_generate(
    path: str = typer.Argument(..., help="Path to file or folder to scan"),
    model_name: str = typer.Option(
        "gpt-4o-mini",
        "--model",
        "-m",
        help=f"Model to use ({', '.join(models)})",
        case_sensitive=False,
    ),
    names: str = typer.Option(
        None,
        "--names",
        "-n",
        help="Comma-separated list of function/class names to process (e.g. 'foo,bar,BazClass')",
    ),
    project: str = typer.Option(
        None,
        "--project",
        "-p",
        help="Root path of the project to index (optional)",
    ),
):
    """
    Automatically scan a folder or file and update docstrings using the selected model.
    Can also process only specific functions or classes.
    """
    if model_name not in models:
        typer.echo(f"❌ Invalid model '{model_name}'. Available: {', '.join(models)}")
        raise typer.Exit(code=1)

    target_names = [n.strip() for n in names.split(",")] if names else None

    typer.echo(f"🔍 Scanning {path} using {model_name}...")
    if target_names:
        typer.echo(f"🎯 Filtering for: {', '.join(target_names)}")
    if project:
        typer.echo(f"🏷 Using project index at: {project}")

    execute_docstring_in_path(
        path=path,
        model_name=model_name,
        target_names=target_names,
        project_path=project,  # for project indexer
    )
