from typer import Typer
from memory_forward.app import hello
from memory_forward.app import goodbye

app = Typer()
app.command()(hello.hello)
app.command()(goodbye.goodbye)

def main():
    app()
