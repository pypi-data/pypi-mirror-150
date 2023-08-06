import typer
from app.helper import hello_world

app = typer.Typer()


@app.command("test")
def test():
    """Prints "Hello World!" (if it works)"""

    typer.echo(hello_world())


@app.command("add")
def add(
    first_num: int = typer.Argument(
        None, help="First number to add", show_default=True
    ),
    second_num: int = typer.Argument(
        None, help="Second number to add", show_default=True
    ),
):
    """Adds two integers together.

    Supply both numbers with arguments.
    """
    total = first_num + second_num

    typer.echo(f"Result is {total}")


def main():
    app()
