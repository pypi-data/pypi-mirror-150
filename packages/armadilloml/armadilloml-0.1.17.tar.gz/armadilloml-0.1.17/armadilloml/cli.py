import os
import time
import uuid
import shutil
import requests
import rich_click as click
from git import Repo
from rich.console import Console
from typing import Optional
from .api_client import create_model, delete_model, ExpiredSession
from .utils import (
    get_armadillo_session,
    get_armadillo_value,
    require_armadillo_project,
    validate_id,
    get_armadillo_url,
    get_armadillo_config,
    add_to_armadillo_config,
    require_session,
    validate_example,
)
from .templating import render_template_directory
from .serving import run, test

console = Console()

pass_env = click.option(
    "--env",
    default="PROD",
    help="The environment to use for the model. Defaults to PRODUCTION.",
)


@click.command()
@pass_env
def login(env: str):
    """
    Login to Armadillo. Under the hood, this creates a session ID in Armadillo
    that is sent to allow follow-up requests. The session ID is saved locally,
    and if the login is successful then we will store it in Firebase
    as a valid session ID. That way, when you use it in follow-up requests,
    we will know that the requests are coming from a trusted source.
    """
    TIME_BETWEEN_REQUESTS = 0.5
    random_id = str(uuid.uuid4())
    armadillo_url = get_armadillo_url(env)
    click.launch(
        f"{armadillo_url}/signin?sessionId={random_id}",
    )
    validating = True
    with console.status("Waiting for you to log in...") as status:
        while validating:
            time.sleep(TIME_BETWEEN_REQUESTS)
            try:
                session_response = requests.get(
                    f"{armadillo_url}/api/sessions/{random_id}"
                )
                session_response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                console.print(
                    f"There was an error while trying to validate the session: {e}",
                    style="red",
                )
                return
            session_status = session_response.json()["sessionStatus"]
            if session_status == "EXISTS":
                user = session_response.json()["user"]
                console.print(
                    f"Successfully logged in as [bold]{user['email']}[/bold]! :thumbs_up:.",
                    style="blue",
                )
                add_to_armadillo_config(
                    {
                        "session": session_response.json()["session"],
                        "user": session_response.json()["user"],
                    }
                )
                return
            elif session_status == "NOT_EXISTS":
                continue
            else:
                raise ValueError(f"Unknown session status: {session_status}")
        click.echo(f"Something went wrong. Please try again.")
    return


@click.command()
@click.argument("path", type=click.Path(), default=None)
@click.option(
    "--id",
    type=str,
    help="The ID of the model to create.",
    prompt="Model ID",
)
@click.option(
    "--description",
    type=str,
    help="The name of the model to create.",
    prompt="Model Description",
)
@click.option(
    "--delete",
    "-d",
    type=bool,
    default=False,
    flag_value=True,
    help="Delete the directory if it already exists.",
)
@click.option(
    "--example",
    type=str,
    help="An example template to start in. Options: transformers",
)
@pass_env
@require_session
def init(
    path: Optional[str],
    id: str,
    description: str,
    delete: bool,
    env: str,
    example: Optional[str],
):
    """
    Initializes the directory structure for a new model.
    """
    validate_id(id)
    if example:
        validate_example(example)
    try:
        model = create_model(id, description, delete, env)
    except ExpiredSession:
        console.print(
            "Your admin session has expired. Please login again with [white bold]armadilloml login[/white bold].",
            style="red",
        )
        return
    path = os.path.join(os.getcwd(), path)
    if os.path.exists(path):
        if delete:
            console.print(
                f":rotating_light: Deleting local directory [bold]{path}[/bold]",
                style="red",
            )
            shutil.rmtree(path)
        else:
            raise click.BadParameter(f"Path {path}/ already exists")
    repo = Repo.clone_from(model.github_url, path)
    user = get_armadillo_config()["user"]
    render_template_directory(
        "templates/project-template/",
        path,
        {
            "model_id": id,
            "model_name": description,
            "name": user["displayName"],
            "email": user["email"],
        },
    )
    if example:
        render_template_directory(f"templates/examples/{example}/", path)
    console.print(
        f":white_check_mark: Successfully created [bold]{path}[/bold]",
        style="green",
    )
    open_in_vscode = click.confirm("Open in VS Code?", abort=False)
    if open_in_vscode:
        os.system(f"code {path}")


@click.command()
def show_session():
    """
    Show the current session ID.
    """
    session = get_armadillo_session()
    if session:
        console.print_json(data=session)
    else:
        console.print("No session. Run `armadillo login` to create one")


@click.command()
@click.argument("path", type=click.Path(), default=None)
@require_session
@pass_env
def delete(path: str, env: str):
    """
    Performs a hard delete of a repository. This will remove the repository
    from Armadillo, delete it from GitHub, and delete the local directory.
    It should be used with extreme caution!
    """
    path = os.path.join(os.getcwd(), path)
    os.chdir(path)
    require_armadillo_project()
    model_id = get_armadillo_value("id")
    if not model_id:
        raise click.ClickException("No model ID found")
    click.confirm(
        f"Are you SURE you want to delete model: {model_id}? This will delete the model permanently from Armadillo and GitHub. This CANNOT be reversed.",
        abort=True,
    )
    delete_model(model_id, environment=env)
    console.print("Model deleted. Deleting local directory...")
    shutil.rmtree(os.getcwd())


@click.group(help="The CLI for managing your ML models.")
def cli():
    """
    Reference for the command line interface. (This is referenced in poetry.toml)
    """
    pass


cli.add_command(login)
cli.add_command(init)
cli.add_command(show_session, name="show-session")
cli.add_command(run)
cli.add_command(test)
cli.add_command(delete)
