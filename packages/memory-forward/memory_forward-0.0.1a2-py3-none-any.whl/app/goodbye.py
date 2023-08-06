import typer

app = typer.Typer()

@app.command()
def goodbye():
    typer.echo("Goodbye")
