from typer import Typer
import hello
import goodbye

app = Typer()
app.command()(hello.hello)
app.command()(goodbye.goodbye)

if __name__ == "__main__":
    app()
