from typing import Optional

import typer

# from predibase.cli_commands import create
# from predibase.cli_commands import list
# from predibase.cli_commands import run
from predibase.cli_commands import delete, deploy, prompt, settings
from predibase.cli_commands.settings import load_settings, save_local_settings
from predibase.cli_commands.utils import set_defaults_from_settings

app = typer.Typer()
# app.add_typer(run.app, name="run")
# app.add_typer(create.app, name="create")
# app.add_typer(list.app, name="list")
app.add_typer(deploy.app, name="deploy")
app.add_typer(delete.app, name="delete")
app.add_typer(prompt.app, name="prompt")
app.add_typer(settings.app, name="settings")


@app.command()
def init(repo: Optional[str] = None, engine: Optional[str] = None, quiet: bool = False):
    if not quiet:
        repo = repo or typer.prompt("Model repository name", default="")
        engine = engine or typer.prompt("Engine name", default="")
    save_local_settings({k: v for k, v in dict(repo=repo, engine=engine).items() if v})


def main():
    set_defaults_from_settings(load_settings())
    app()


if __name__ == "__main__":
    main()
