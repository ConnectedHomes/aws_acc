from urllib.parse import parse_qs
from chalice import Chalice, AuthResponse
from chalicelib import db
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

@app.route("/awsacc/{accno}", methods=["GET"] )
def get_account(accno):
    return get_app_db().get_item(accno)

@app.route("/awsacc", methods=["POST"])
def add_new_account():
    body = app.current_request.json_body
    # accitem = {}
    # accitem[ "AccountNumber" ] = body[ "AccountNumber" ]
    # accitem[ 'AccountName' ] = body['AccountName']
    # accitem[ 'Active' ] = body['Active']
    # accitem[ 'Description' ] = body[ 'Description' ]
    # accitem[ 'RealUsers ' ] = body[ 'RealUsers' ]
    # accitem[ 'AccOwners' ] = body[ 'AccOwners' ]
    # accitem[ 'OwnerTeam' ]= body[ 'OwnerTeam' ]
    # accitem[ 'PreviousName' ]= body[ 'PreviousName' ]
    # accitem[ 'SecOpsEmail' ]= body[ 'SecOpsEmail' ]
    # accitem[ 'SecOpsSlackChannel' ]= body[ 'SecOpsSlackChannel' ]
    # accitem[ 'TeamEmail'] = body[ 'TeamEmail']
    return get_app_db().add_item(body)


@app.route("/awsacc/{accno}", methods=["DELETE"])
def delete_account(accno):
    print(f"DELETE Account: {accno} ")
    return get_app_db().delete_item( AccountNumber=accno)


@app.route("/awsacc/{accno}", methods=["PUT"])
def update_account(accno):
    body = app.current_request.json_body
    print(type(body))
    get_app_db().update_item( accno, body)
        # Description=body.get("Description"),
        # Active=body.get("Active"),
        # metadata=body.get("metadata")
