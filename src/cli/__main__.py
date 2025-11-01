import typer
from src.cli.docstring_cli import docstring_app
#from src.unity_cli import app as unity_app   #TODO

app = typer.Typer(help="LLM-based developer tools CLI")

# register subcomands
app.add_typer(docstring_app, name="docstring")
#app.add_typer(unity_app, name="unity") #TODO

if __name__ == "__main__":
    app()
