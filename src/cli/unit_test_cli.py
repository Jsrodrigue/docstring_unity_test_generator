import typer
from src.unit_test_core.unit_test_executor import execute_unit_test_in_path
from constants import models
import asyncio

unit_test_app = typer.Typer(help="Automatic pytest unit test generator")

@unit_test_app.command("generate")
def scan_and_generate_tests(
    path: str = typer.Argument(..., help="Path to file or folder to scan for code"),
    project_path: str = typer.Argument(..., help="Root path of the project to index"),
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
):
    """
    Automatically scans a specified folder or file to generate pytest unit tests
    using the selected model.

    Args:
      path (str): File or folder containing Python code.
      project_path (str): Root path of the project to index (mandatory).
      model_name (str): Model to use for test generation. Default: gpt-4o-mini.
      names (str): Optional comma-separated list of function or class names.
    """
    if model_name not in models:
        typer.echo(f"❌ Invalid model '{model_name}'. Available: {', '.join(models)}")
        raise typer.Exit(code=1)

    target_names = [n.strip() for n in names.split(",")] if names else None

    typer.echo(f"🧪 Generating unit tests for {path} using {model_name}...")
    typer.echo(f"🏷 Using project index at: {project_path}")
    if target_names:
        typer.echo(f"🎯 Filtering for: {', '.join(target_names)}")

    asyncio.run(
        execute_unit_test_in_path(
        path=path,
        model_name=model_name,
        target_names=target_names,
        project_path=project_path,
        )
    )
    
