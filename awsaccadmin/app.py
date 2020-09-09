from urllib.parse import parse_qs
from chalice import Chalice, AuthResponse
from chalicelib import db, auth
import boto3
import os
import json
from ast import literal_eval

app = Chalice(app_name="awsaccadmin")
app.debug = True
_DB = None
_USER_DB = None

def get_app_db():
    global _DB
    if _DB is None:
        _DB = db.DynamoDBAWSAcc(
            boto3.resource("dynamodb").Table(os.environ["APP_TABLE_NAME"]) )
    return _DB

def get_users_db():
    global _USER_DB
    if _USER_DB is None:
        _USER_DB = boto3.resource("dynamodb").Table(os.environ["USERS_TABLE_NAME"])
    return _USER_DB

@app.route("/awsacc", methods=["GET"])
def get_awsacc():
    return get_app_db().list_items()

@app.route("/awsacc/all", methods=["GET"])
def get_awsacc():
    return get_app_db().list_all_items()

@app.route("/awsacc", methods=["POST"])
def add_new_account():
    body = app.current_request.json_body
    return get_app_db().add_item(
        description=body["Description"],
        metadata=body.get("metadata"),
        AccountNumber = body["AccountNumber"],
        AccountName = body["AccountName"]
    )

@app.route("/awsacc/{accno}", methods=["GET"])
def get_account(accno):
    return get_app_db().get_item(accno)


@app.route("/awsacc/{uid}", methods=["DELETE"])
def delete_todo(uid):
    return get_app_db().delete_item(uid)


@app.route("/awsacc/{uid}", methods=["PUT"])
def update_todo(uid):
    body = app.current_request.json_body
    get_app_db().update_item(
        uid,
        description=body.get("description"),
        state=body.get("state"),
        metadata=body.get("metadata"))

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to "/".
#
# Here are a few more examples:
#
# @app.route("/hello/{name}")
# def hello_name(name):
#    # "/hello/james" -> {"hello": "james"}
#    return {"hello": name}
#
# @app.route("/users", methods=["POST"])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We"ll echo the json body back to the user in a "user" key.
#     return {"user": user_as_json}
#
# See the README documentation for more examples.
#
