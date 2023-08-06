"""
This module deals with serving the actual models. It implements a layer on top
of Flask that has some built-in logic and error handling. The reason we need 
this is so that 1) data scientists don't need to do extra work to build a 
Flask server and 2) all Armadillo models can follow some standard conventions
for what type of data they accept and how they handle errors.
"""

import os
import sys
import rich_click as click
from rich.console import Console
from flask import Flask, request, jsonify
from .utils import require_armadillo_project

console = Console()


@click.command()
@click.argument("path", type=click.Path(), default=None)
def run(path: str):
    """
    Run the Armadillo model server. This command is meant to be run within an
    Armadillo project. It will look for the `predict` function in the `app.py`
    file and then run that function
    """

    server = Flask(__name__)

    path = os.path.join(os.getcwd(), path)
    require_armadillo_project(path)
    try:
        sys.path.append(path)
        from app import predict

    except ImportError:
        raise click.ClickException(
            "You must have a predict function in your Armadillo project."
        )
    if not callable(predict):
        raise click.ClickException(
            "The `predict` function must be a function."
        )
    server = Flask(__name__)

    @server.route("/", methods=["POST"])
    def predict_route():
        """
        This is the route that the Armadillo model server will use to make
        predictions.
        """
        request_payload = request.json
        if not request_payload:
            return jsonify({"error": "No request payload provided."}), 400
        if "input" not in request_payload:
            return (
                jsonify(
                    {"error": "Request payload must contain and `input`."}
                ),
                400,
            )
        try:
            result = predict(request_payload["input"])
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        return jsonify(result)

    @server.errorhandler(405)
    def method_not_allowed(e):
        return (
            jsonify(
                {
                    "error": f"Method {request.method } not allowed. Only POST requests."
                }
            ),
            405,
        )

    server.run(
        debug=False,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
    )


@click.command()
@click.argument("path", type=click.Path(), default=None)
def test(path: str):
    """
    Runs the test function from the app.
    """
    path = os.path.join(os.getcwd(), path)
    require_armadillo_project(path)
    try:
        sys.path.append(path)
        from app import test

    except ImportError:
        raise click.ClickException(
            "You must have a predict function in your Armadillo project."
        )
    if not callable(test):
        raise click.ClickException(
            "The `predict` function must be a function."
        )
    return test()
