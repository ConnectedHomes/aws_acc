import json
import requests
import argparse

# 1) Get default AWS Account (mode=None, accno=None)
# 2) et all active AWS accounts (mode="all", accno=None)
# 3) Get all AWS accounts ever, including inactive (mode="allever", accno=None)
# 4) Get one numbered AWS account (mode=None, accno=acno)
# 5) Add an account with the supplied parameters

#baseurl = "https://ta6lpu0e8g.execute-api.eu-west-1.amazonaws.com/api"
baseurl = "https://qbof269pb2.execute-api.eu-west-1.amazonaws.com/api"
# baseurl = "http://localhost:8000"
headers = {'Content-Type': 'application/json', }
api_url = '{}/awsacc'.format(baseurl)

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

parser = argparse.ArgumentParser()
parser.add_argument("--accno",
                    help="use an account number to get details about a specific account.",
                    default=None)
parser.add_argument("--mode", help="use an mode.", default=None)
parser.add_argument("--accname", help="AWS Account Name", default=None)
parser.add_argument("--active", help="Boolean showing live status.", default="N")
parser.add_argument("--deleted", help="Boolean to get deleted accounts.", default="N")
parser.add_argument("--desc", help="Description of AWS Account.", default=None)
parser.add_argument("--realusers", help="Account contains REAL USER data.  For GDPR Purps.", default="N")
parser.add_argument("--accowners", help="Comma delimited list of account owners.", default=None)
parser.add_argument("--ownerteam", help="Internal Team owning AWS Account", default=None)
parser.add_argument("--prevname", help="Any former names for this AWS Account", default=None)
parser.add_argument("--teamemail", help="Email address to notify team for this account.", default=None)
parser.add_argument("--secopsemail", help="Email address for security notifications for this account.", default=None)
parser.add_argument("--secopsslack", help="Slack Channel for security notifications for this account.", default=None)
args = parser.parse_args()


def make_dict_from_args(args):
    params = {}
    for key in vars(args):
        value = getattr(args, key)
        if key != "mode":
            newkeyname = inverse_account_keys[key]
            params[newkeyname] = value
    return params

def eval_command(args):
    account_details = []
    params = {}
    api_url = '{}/awsacc'.format(baseurl)
    headers = {'Content-Type': 'application/json'}
    if args.mode == "add":
        params = make_dict_from_args(args)
        response = requests.post(api_url, headers=headers, data=json.dumps(params))
        account_details.append(response.content)

    elif args.mode == "update":
        api_url = '{}/awsacc/{}'.format(baseurl, args.accno)
        params = make_dict_from_args(args)
        response = requests.put(api_url, headers=headers, data=json.dumps(params))
        account_details.append(response.content)

    elif args.mode == "search":  # 2, 3
        api_url = '{}/awsacc/{}'.format(baseurl, args.mode)
        response = requests.get(api_url, headers=headers, params=params)

        if args.accno is not None:       # 4
            api_url = '{}/awsacc'.format(baseurl)
            response = requests.get(api_url, headers=headers, params=params)
        else:
            if args.deleted == "Y":
                api_url = '{}/awsacc/alldeleted'.format(baseurl)  # 1
                response = requests.get(api_url,headers=headers,params=params)
            else:
                api_url = '{}/awsacc/alllive'.format(baseurl) # 1
                response = requests.get(api_url, headers=headers, params=params)

    print(response.content)

    if response.status_code == 200:
        if "not found." in str(response.content):
            account_details.append(response.content)
        else:
            for acc in response.json():
                account_details.append(acc)
    elif response.status_code == 403:
        print(f"403 Forbidden.  Try renewing your chaim credentials.")
    elif response.status_code == 400:
        print(f"400 Bad Request.  Check your request.")
        # print(response.request)
    else:
        print(response.status_code)
        account_details = []
    return account_details

def go():
    if args.mode is None:
        args.mode = "search"

    print(f"Process request for mode {args.mode} AWS Account {args.accno}.")
    account_info = eval_command(args)
    print(f"Accountrequest {account_info}")

    # if account_info is not None:
    #     if len(account_info) == 1:
    #         print(f"Accountrequest: {account_info} ")
    #         # print(f"Account request: {json.dumps(account_info[0], sort_keys=True, indent=4)} ")
    #     else:
    #         for c, x in enumerate(account_info):
    #             print(f"Accountrequest: ")
    #             print(c, json.dumps(c, sort_keys=True, indent=4))
    # else:
    #     print('[!] Request Failed')
go()