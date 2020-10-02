from chalice import Chalice
from chalicelib import db
from urllib.parse import urlparse, parse_qs
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
    return get_app_db().list_accounts()

@app.route("/awsacc/all", methods=["GET"])
def get_awsacc():
    accounts = get_app_db().list_live_accounts()
    return accounts, f"Count: {len(accounts)}"

@app.route("/awsacc/allever", methods=["GET"])
def get_awsacc():
    accounts = get_app_db().list_all_accounts()
    return accounts, f"Count: {len(accounts)}"

@app.route("/awsacc/{accno}", methods=["GET"] )
def get_account(accno):
    return get_app_db().get_account(accno)

@app.route("/awsacc", methods=["POST"], content_types=['application/json'])
def add_new_account():
    body = app.current_request.json_body
    response = get_app_db().add_account(body)
    return response

@app.route("/awsacc/{accno}", methods=["DELETE"])
def delete_account(accno):
    print(f"DELETE Account: {accno} ")
    # return get_app_db().delete_account( AccountNumber=accno)
    return get_app_db().toggle_account_active( AccountNumber=accno, Active="N")

@app.route("/awsacc/{accno}", methods=["PUT"], content_types=['application/json'])
def update_account(accno):
    body = app.current_request.json_body
    response = get_app_db().update_account(accno, body)
    return response
