import json
import os
from pathlib import Path
from typing import Any, Dict

import typer
from rich import print

APP_NAME = "predibase-sdk-app"
LOCAL_SETTINGS_NAME = ".predibase.json"

app = typer.Typer()


@app.command()
def show_global():
    settings = load_global_settings()
    print(settings)


@app.command()
def show_local():
    settings = load_local_settings()
    print(settings)


@app.command()
def show():
    settings = load_settings()
    print(settings)


@app.command()
def set_repo(repo: str):
    _set_setting("repo", repo)


@app.command()
def set_engine(engine: str):
    _set_setting("engine", engine)


@app.command()
def set_token(token: str):
    _set_setting("token", token)


@app.command()
def set_endpoint(endpoint: str):
    _set_setting("endpoint", endpoint)


def _set_setting(setting: str, value: Any):
    settings = load_global_settings()
    settings[setting] = value
    save_global_settings(settings)


def get_global_settings_path() -> Path:
    app_dir = typer.get_app_dir(APP_NAME)
    return Path(app_dir) / "settings.json"


def save_global_settings(settings: Dict[str, Any]):
    settings_path = get_global_settings_path()
    os.makedirs(settings_path.parent, exist_ok=True)
    with open(settings_path, "w") as f:
        json.dump(settings, f)


def load_global_settings() -> Dict[str, Any]:
    settings_path = get_global_settings_path()
    if settings_path.is_file():
        with open(settings_path) as f:
            return json.load(f)
    return {}


def save_local_settings(settings: Dict[str, Any]):
    settings_path = Path(LOCAL_SETTINGS_NAME)
    os.makedirs(settings_path.parent, exist_ok=True)
    with open(settings_path, "w") as f:
        json.dump(settings, f)


def load_local_settings() -> Dict[str, Any]:
    settings_path = Path(LOCAL_SETTINGS_NAME)
    if settings_path.is_file():
        with open(settings_path) as f:
            return json.load(f)
    return {}


def load_settings() -> Dict[str, Any]:
    local_settings = load_local_settings()
    global_settings = load_global_settings()
    return {**global_settings, **local_settings}
