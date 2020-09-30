import json
import requests
import argparse

# 1) Get default AWS Account (mode=None, accno=None)
# 2) et all active AWS accounts (mode="all", accno=None)
# 3) Get all AWS accounts ever, including inactive (mode="allever", accno=None)
# 4) Get one numbered AWS account (mode=None, accno=acno)
# 5) Add an account with the supplied parameters

# baseurl = "https://ic5jbzort7.execute-api.eu-west-1.amazonaws.com/api"
baseurl = "http://localhost:8000"
headers = {'Content-Type': 'application/json', }
body = {'AccOwners': "Deborah Balm", 'AccountName': "DebsDemoAccount", 'AccountNumber': "0957654321", 'Active': "N",
        'Description': "A Demo Account Add", 'OwnerTeam': "SRE", 'PreviousName': None, 'RealUsers': "N",
        'SecOpsEmail': "sre@hivehome.com", 'SecOpsSlackChannel': "#ops-chat", 'TeamEmail': "sre@hivehome.com"}


def go():
    api_url = '{}/awsacc'.format(baseurl)
    print(f"Body {body} type {type(body)}")
    response = requests.post(api_url, headers=headers, data=json.dumps(body))
    print(f"response.content {response.content}")

go()