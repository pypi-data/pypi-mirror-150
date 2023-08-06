try:
    import typer
except ImportError as e:
    raise RuntimeError(
        "The command-line application requires typer to be installed. Install adviceslip[cli] with pip or conda."
    ) from e

from typing import Optional

from .client import Client

app = typer.Typer()


@app.command()
def random() -> None:
    with Client() as client:
        slip = client.random()
    typer.echo(slip)


@app.command()
def id(id: int) -> None:
    with Client() as client:
        slip = client.slip_from_id(id)
    typer.echo(slip)


@app.command()
def search(query: str) -> None:
    with Client() as client:
        search = client.search(query)
    for slip in search:
        typer.echo(slip)
