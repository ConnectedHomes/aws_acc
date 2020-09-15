from chalice import Chalice
from chalicelib import db
import boto3
import os
import json

app = Chalice(app_name="awsaccadmin")
app.debug = True
_DB = None

def get_app_db():
    global _DB
    if _DB is None:
        _DB = db.DynamoDBAWSAcc(
            boto3.resource("dynamodb").Table(os.environ["APP_TABLE_NAME"]) )
    return _DB

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
