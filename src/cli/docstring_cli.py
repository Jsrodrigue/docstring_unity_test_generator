import typer
from constants import models
from src.docstring_core.docstring_generator import generate_from_path_dict
import asyncio
from pathlib import Path

docstring_app = typer.Typer(help="Python docstring auto-generator and updater")

@docstring_app.command()
def scan_and_generate(
    path: str = typer.Argument(..., help="Path to file or folder to scan"),
    model_name: str = typer.Option(
        "gpt-4o-mini",
        "--model", "-m",
        help=f"Model to use ({', '.join(models)})",
        case_sensitive=False,
    ),
    names: str = typer.Option(
        None,
        "--names", "-n",
        help="Comma-separated list of function/class names to process (e.g. 'foo,bar,BazClass')",
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

    results = asyncio.run(generate_from_path_dict(path, model_name=model_name, target_names=target_names))
    if not results:
        typer.echo("❌ No docstrings generated.")
        return

    from src.docstring_core.docstring_updater import update_docstrings
    for item in results:
        update_docstrings(Path(item["file_path"]), [item])
    
    typer.echo(f"✅ Updated {len(results)} item(s).")

