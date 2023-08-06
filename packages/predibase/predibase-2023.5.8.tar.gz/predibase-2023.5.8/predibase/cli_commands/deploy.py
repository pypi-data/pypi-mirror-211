import re
from typing import Optional

import typer

from predibase.cli_commands.utils import get_client, get_console

app = typer.Typer()


# TODO(travis): this should be dynamic based on model type and pushed to the backend
DEFAULT_TEMPLATE = "llm-gpu-small"


@app.command()
def llm(
    name: str = typer.Argument(None, help="Name of the model"),
    model_name: str = typer.Argument(None, help="Name of the model"),
    engine_template: Optional[str] = typer.Option(
        DEFAULT_TEMPLATE,
        "--engine-template",
        "-e",
        help="Engine template to provision for hosting the model",
    ),
    # auto_suspend_secs: Optional[int] = 3600,  # TODO: add ability to auto suspend
):
    if name is None:
        raise ValueError("name is required")

    if model_name is None:
        raise ValueError("model_name is required")

    # raise ValueError if name is not lower case alphanumeric characters or '-'
    if re.match(r"^[a-z0-9-]+$", name) is None:
        raise ValueError("name must be lower case alphanumeric characters or '-'")

    client = get_client()

    get_console().print("Deploying an LLM with the following parameters:")
    get_console().print("\tname:", name)
    get_console().print("\tmodel_name:", model_name)
    get_console().print("\tengine_template:", engine_template)

    client.session.post_json("/llms", json={"name": name, "modelName": model_name, "engineTemplate": engine_template})
    get_console().print("Deploy request sent.")


if __name__ == "__main__":
    app()
