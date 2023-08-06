import os
import json
import rich_click as click
import pkg_resources
from typing import Union, Optional
from rich.console import Console
from functools import wraps

APP_NAME = "ArmadilloML"
console = Console()


def find_armadillo_config():
    """
    Find the config file for the CLI. It's different on every machine.
    (If it doesn't exist, it makes one for you.)
    """
    app_dir = click.get_app_dir(APP_NAME)
    if not os.path.exists(app_dir):
        os.makedirs(app_dir)
    config_file = os.path.join(app_dir, "armadillo-config.json")
    return config_file


def require_session(func: callable):
    """
    Command decorator that checks that the user has a session ID.
    Make sure to use this as the final decorator to your click command!
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not get_armadillo_session():
            raise click.BadParameter(
                "You must be logged in to use this command."
                "Use `armadillo login` to log in."
            )
        return func(*args, **kwargs)

    return wrapper


def get_armadillo_url(env: str) -> str:
    """
    Get the armadillo url for the given environment.
    """
    if env in ("PROD", "PRODUCTION", "prod", "production"):
        return "https://www.witharmadillo.com/"
    elif env == "STAGING":
        # TODO: Make this URL work for real.
        return "https://staging.armadillo.ml"
    elif env in ("DEV", "DEVELOPMENT", "dev", "development"):
        return "http://localhost:3000"
    else:
        raise ValueError(f"Unknown environment: {env}")


def get_armadillo_config() -> dict:
    """
    Load the Armadillo Config JSON File. This is a global application file
    that stores data about the Armadillo CLI. Right now it just stores a
    Session ID and some user data and stuff like that. You can read more about
    application files here:
    https://click.palletsprojects.com/en/7.x/utils/#finding-application-folders
    """
    config_file = find_armadillo_config()
    if not os.path.exists(config_file):
        with open(config_file, "w") as f:
            f.write("{}")
        return {}
    else:
        with open(config_file, "r") as f:
            return json.load(f)


def add_to_armadillo_config(new_config: dict) -> dict:
    """
    Merges a new dictionary with the underlying Armadillo config. This will
    overwrite existing values but not delete anything. Returns the new merged
    dictionary.
    """
    current_config = get_armadillo_config()
    merged_config = {**current_config, **new_config}
    config_file = find_armadillo_config()
    with open(config_file, "w") as f:
        json.dump(merged_config, f, indent=4)
        return merged_config


def get_armadillo_session() -> Union[str, None]:
    """
    Load the Armadillo Session Object, if there is one.
    """
    return get_armadillo_config().get("session", None)


def validate_id(model_id: str):
    """Validates that the ID contains no spaces or special characters."""
    if not model_id:
        raise click.BadParameter("ID cannot be empty")
    if " " in model_id:
        raise click.BadParameter("ID cannot contain spaces")
    return model_id


def require_armadillo_project(path: Optional[str] = None):
    """
    Checks that the current directory is an Armadillo project.
    """
    if not path:
        path = os.getcwd()
    else:
        path = os.path.abspath(path)
    if not os.path.exists(os.path.join(path, "armadillo.json")):
        raise click.BadParameter("Not in an Armadillo project.")
    if not os.path.exists(os.path.join(path, ".git")):
        raise click.BadParameter("Not in an Armadillo project.")


def set_armadillo_value(key: str, value: str):
    """
    Saves a value to armadillo.json in the local project.
    """
    with open("armadillo.json") as f:
        data = json.load(f)
    data[key] = value
    with open("armadillo.json", "w") as f:
        json.dump(data, f, indent=4)


def get_armadillo_value(key: str):
    """
    Gets a value from armadillo.json in the local project.
    """
    with open("armadillo.json") as f:
        data = json.load(f)
    return data[key]


def validate_example(example: str):
    """
    Validates that the example is a valid example.
    """
    examples = pkg_resources.resource_listdir(__name__, "templates/examples")
    if example not in examples:
        examples_str = ", ".join(examples)
        raise click.BadParameter(
            f"{example} is not a valid example. Choose one of: {examples_str}"
        )
    return True
