import typer
from app.helper import hello_world

app = typer.Typer()


@app.command("test")
def test():
    """Prints "Hello World!" (if it works)"""

    typer.echo(hello_world())


@app.command("add")
def add():
    """Prints add"""

    typer.echo("Add")


def main():
    app()
