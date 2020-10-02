import json
import requests
import argparse

# 1) Get default AWS Account (mode=None, accno=None)
# 2) et all active AWS accounts (mode="all", accno=None)
# 3) Get all AWS accounts ever, including inactive (mode="allever", accno=None)
# 4) Get one numbered AWS account (mode=None, accno=acno)
# 5) Add an account with the supplied parameters

baseurl = "https://ic5jbzort7.execute-api.eu-west-1.amazonaws.com/api"
# baseurl = "http://localhost:8000"
headers = {'Content-Type': 'application/json', }
args = {"mode": "add",
        "accno": "2987734329",
        "accname": "DebsDemoAccount",
        "active": "N" ,
        "desc": "A Demo Account Add",
        "realusers": "N",
        "accowners": "Deborah Balm",
        "ownerteam": "SRE",
        "teamemail": "sre@hivehome.com",
        "secopsemail": "sre@hivehome.com",
        "secopsslack": "#ops-chat"
         }
body = {'AccOwners': "Deborah Balm", 'AccountName': "DebsDemoAccount", 'AccountNumber': "0957654321", 'Active': "N",
        'Description': "A Demo Account Add", 'OwnerTeam': "SRE", 'PreviousName': None, 'RealUsers': "N",
        'SecOpsEmail': "sre@hivehome.com", 'SecOpsSlackChannel': "#ops-chat", 'TeamEmail': "sre@hivehome.com"}

account_keys = {
          "AccOwners": "accowners",
          "AccountName": "accname",
          "AccountNumber": "accno",
          "Active": "active",
          "Description": "desc",
          "OwnerTeam": "ownerteam",
          "PreviousName": "prevname",
          "RealUsers": "realusers",
          "SecOpsEmail": "secopsemail",
          "SecOpsSlackChannel": "secopsslack",
          "TeamEmail": "teamemail"
          }
inverse_account_keys = {v: k for k, v in account_keys.items()}

def make_dict_from_args(args):
    params = {}
    del args['mode']
    for key, value in args.items():
        newkeyname = inverse_account_keys[key]
        params[newkeyname] = value
    return params

def go():
    api_url = '{}/awsacc'.format(baseurl)
    print(f"Body {args} type {type(args)}")
    params = make_dict_from_args(args)
    print(f"response.content {params}")
    response = requests.post(api_url, headers=headers, data=json.dumps(body))
    print(f"response.content {response.content}")

go()