import os
from pathlib import Path
import boto3
import csv
from chalicelib import db
import sys

account = sys.argv[1]
region = "eu-west-1"
destination_table = "AWSAccountAdmin"
session = boto3.Session(profile_name=account, region_name=region)
dynamodb_resource = session.resource('dynamodb')
basedir = os.getcwd()
dcsv = "Confluence-Owners-AWS-Deleted-Accounts.csv"
acsv = "Confluence-Owners-AWS.csv"
_DB = None

def in_dictlist(key, value, my_dictlist):
    for this in my_dictlist:
        if this[key] == value:
            return this
    return {}

def convert_csv_to_json_list(file):
   items = []
   with open(file) as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
          print(row)
          # print(type(row))
          if in_dictlist('AccountNumber', row[ 'Acc No' ], items ):
              print(f"{row[ 'Acc No' ]} already in items")
          else:
              # print(row)
              data = {}
              data[ 'AccountNumber' ] = row[ 'Acc No' ]
              data[ 'AccountName' ] = row[ 'Account Name' ]
              data[ 'Description' ] = row[ 'Description' ]
              data[ 'RealUsers' ] = row[ 'Real Users' ]
              data[ 'Active' ] = 'N'
              if 'Owning Team' in row:
                  data[ 'Active' ] = 'Y'
                  data[ 'OwnerTeam' ] = row[ 'Owning Team' ]
                  data[ 'TeamEmail' ] = row[ 'Team Email' ]
                  data[ 'PreviousName' ] = row[ 'Previously named' ]
                  data[ 'SecOpsEmail' ] = row[ '  Security/Operations Contact Email ' ]
                  data[ 'SecOpsSlackChannel' ] = row[ 'Security/Operations Slack Channel' ]
                  data[ 'AccOwners' ] = row[ 'Account Owner(s)' ]
              items.append(data)

   return items

def batch_write(items):
   db = dynamodb_resource.Table(destination_table)
   with db.batch_writer() as batch:
      for item in items:
         batch.put_item(Item=item)

def add_account_as_item():
    body = app.current_request.json_body
    return get_app_db().add_item(
        description=body["Description"],
        metadata=body.get("metadata"),
        Active="Y",
        AccountNumber = body["AccountNumber"],
        AccountName = body["AccountName"]
    )

def go():
    for csv in [dcsv, acsv]:
        file = Path(f'{basedir}/{csv}')
        print(f'Importing {file}')
        json_data = convert_csv_to_json_list(file)
        # print(json_data)
        batch_write(json_data)

go()