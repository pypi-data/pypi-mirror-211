import typer

from predibase.cli_commands.utils import get_client, get_console

app = typer.Typer()


@app.command()
def llm(
    name: str = typer.Argument("name", help="Name of the model"),
):
    if name is None:
        raise ValueError("name is required")

    client = get_client()

    get_console().print(f"Deleting LLM with name: {name}")

    client.session.delete_json(f"/llms/{name}")
    get_console().print("Delete request sent.")


if __name__ == "__main__":
    app()
