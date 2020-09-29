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

parser = argparse.ArgumentParser()
parser.add_argument("--accno",
                    help="use an account number to get details about a specific account.",
                    default=None)
parser.add_argument("--mode", help="use an mode.", default=None)
parser.add_argument("--accname", help="AWS Account Name", default=None)
parser.add_argument("--active", help="Boolean showing live status.", default="N")
parser.add_argument("--desc", help="Description of AWS Account.", default=None)
parser.add_argument("--realusers", help="Account contains REAL USER data.  For GDPR Purps.", default="N")
parser.add_argument("--accowners", help="Comma delimited list of account owners.", default=None)
parser.add_argument("--ownerteam", help="Internal Team owning AWS Account", default=None)
parser.add_argument("--prevname", help="Any former names for this AWS Account", default=None)
parser.add_argument("--teamemail", help="Email address to notify team for this account.", default=None)
parser.add_argument("--secopsemail", help="Email address for security notifications for this account.", default=None)
parser.add_argument("--secopsslack", help="Slack Channel for security notifications for this account.", default=None)
args = parser.parse_args()


def eval_command(accno, mode):
    account_details = []
    params = {}

    if args.mode == "add":
        print(f"In add for {args.accno}")
        params = json.dumps({   "AccOwners": args.accowners,
                        "AccountName": args.accname,
                        "AccountNumber": args.accno,
                        "Active": args.active,
                        "Description": args.desc,
                        "OwnerTeam": args.ownerteam,
                        "PreviousName": args.prevname,
                        "RealUsers": args.realusers,
                        "SecOpsEmail": args.secopsemail,
                        "SecOpsSlackChannel": args.secopsslack,
                        "TeamEmail": args.teamemail,
        })

        api_url = '{}/awsacc'.format(baseurl)
        # api_url = 'http://localhost:8000/awsacc'
        print(api_url)
        print(f"Params {params}")

        response = requests.post(api_url, headers=headers, params=params)

        account_details.append(response.content)
        print(f"response.content {response.content}")


    elif args.mode == "search":  # 2, 3
        api_url = '{}/awsacc/{}'.format(baseurl, args.mode)
        response = requests.get(api_url, headers=headers, params=params)

        if args.accno is not None:       # 4
            api_url = '{}/awsacc/{}'.format(baseurl, args.accno)
            response = requests.get(api_url, headers=headers, params=params)
        else:
            api_url = '{}/awsacc'.format(baseurl)  # 1
            response = requests.get(api_url, headers=headers, params=params)

    print(response)
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
        print(response.request)
    else:
        print(response.status_code)
        # account_details = []
    return account_details

def go():
    if args.mode is None:
        args.mode = "search"

    print(f"Process request for mode {args.mode} AWS Account {args.accno}.")
    # print(f"Accno {args.accno}, Mode {args.mode}")
    account_info = eval_command(args.accno, args.mode)
    print(f"Account request {account_info}")

    if account_info is not None:
        if len(account_info) == 1:
            print(f"Account request: {account_info} ")
            print(f"Account request: {json.dumps(account_info[0], sort_keys=True, indent=4)} ")
        else:
            for c, x in enumerate(account_info):
                print(f"Account request: ")
                print(c, json.dumps(c, sort_keys=True, indent=4))
    else:
        print('[!] Request Failed')


go()