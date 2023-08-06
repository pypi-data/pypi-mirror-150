"""
Utilities for interacting with the Armadillo Admin API.
"""

import urllib
import requests
import rich_click as click
from rich.console import Console
from .types import Model
from .exceptions import ExpiredSession, APIException
from ..utils import get_armadillo_url, get_armadillo_session

console = Console()


def get_model(model_id: str, environment: str = "PRODUCTION"):
    """
    Get information about a model from the Armadillo Admin API.
    """
    armadillo_url = get_armadillo_url(environment)
    response = requests.get(f"{armadillo_url}/api/admin/models/{model_id}")
    return response.json()


def delete_model(model_id: str, environment: str = "PRODUCTION"):
    """
    Delete a model using the Armadillo Admin API.
    """
    armarmillo_url = get_armadillo_url(environment)
    session = get_armadillo_session()
    if not session:
        raise click.ClickException(
            "No session ID found. Something is wrong (this should have been caught by the decorator)."
        )
    response = requests.delete(
        f"{armarmillo_url}/api/admin/models/{model_id}",
        cookies={"token": session["token"]},
    )
    response.raise_for_status()
    return response.json()


def create_model(
    model_id: str,
    description: str,
    delete_existing: bool = False,
    environment: str = "PRODUCTION",
) -> Model:
    """
    Create a model repository with the Armadillo Admin API.
    Args:
       model_id: The ID of the model.
       description: The description of the model.
       delete_existing: Delete the existing repository if it exists. (Will prompt you.)
    """
    armadillo_url = get_armadillo_url(environment)
    session = get_armadillo_session()
    if not session:
        raise Exception(
            "No session ID found. Something is wrong (this should have been caught by the decorator)."
        )
    response = requests.post(
        f"{armadillo_url}/api/admin/models",
        json={"id": model_id, "description": description},
        cookies={"token": session["token"]},
    )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        if response.status_code in (404, 400):
            raise click.ClickException(
                "Cannot access the Armadillo server. Did you forget to pass the --env flag?"
            )
        elif response.status_code == 500:
            raise click.ClickException(
                "The Armadillo server encountered an internal error. Try again later."
            )
        try:
            rj = response.json()
        except requests.exceptions.JSONDecodeError:
            # This (usually) means that the admin cookie has expired.
            # TODO: Make this more explicit in the API.
            raise ExpiredSession()
        if rj.get("code") == "MODEL_ALREADY_EXISTS":
            if not delete_existing:
                raise click.BadParameter(
                    f"Model repository {model_id} already exists."
                )
            else:
                console.print(
                    f"[red]:rotating_light: Model repository [bold]{model_id}[/bold] already exists, but you have opted to delete it.[/red]"
                )
                click.confirm(
                    "Are you sure you want to delete it?", abort=True
                )
                delete_model(model_id, environment)
                console.print(
                    f":white_check_mark: Deleted remote repository [bold]{model_id}[/bold].",
                    style="green",
                )
                return create_model(
                    model_id, description, delete_existing, environment
                )
    console.print(
        f":white_check_mark: Created {'[italic](new)[/italic] ' if delete_existing else ''}remote repository [bold]{model_id}[/bold] @",
        style="green",
    )
    model_url = urllib.parse.urljoin(
        armadillo_url, f"/admin/models/{model_id}"
    )
    console.print(
        f"{model_url}",
        style="blue",
    )
    model_data = response.json().get("modelData")
    if not model_data:
        raise click.ClickException(
            "Something went wrong during model creation. Try again later."
        )
    model = Model(
        id=model_data["id"],
        description=model_data["description"],
        parent_user_id=model_data["parentUserId"],
        github_url=model_data["githubURL"],
    )
    return model


def get_requests(endpoint: str, environment: str = "PRODUCTION"):
    """
    Get the requests for a given endpoint.
    Args:
        endpoint (str): The endpoint to get requests for. Must contain the
            full path e.g. mdavish/my-endpoint
        environment (str): The environment to get requests for.
    """

    raise NotImplementedError("This is not implemented yet.")

    # TODO Impelement this once we have an endpoint for listings all requests
    # including pagination etc.

    session = get_armadillo_session()
    armadillo_url = get_armadillo_url(environment)
    endpoint_url = urllib.join(armadillo_url, "api", endpoint, "requests")
    response = requests.get(endpoint_url, cookies={"token": session["token"]})
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        raise APIException("Something went wrong.")
    return response.json()
