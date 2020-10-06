from uuid import uuid4
# import json
from boto3.dynamodb.conditions import Key, Attr

DEFAULT_ACCOUNTNUMBER = '039759963043'

class AWSAccDB(object):
    def list_accounts(self):
        pass

    def list_all_accounts(self):
        pass

    def list_live_accounts(self):
        pass

    def list_deleted_accounts(self):
        pass

    def get_account(self, AccountNumber):
        pass

    def add_account(self):
        pass

    def delete_account(self, AccountNumber):
        pass

    def update_account(self, AccountNumber, jsonbody):
        pass

    def toggle_account_active(self, AccountNumber, Active):
        pass


class DynamoDBAWSAcc(AWSAccDB):
    def __init__(self, table_resource):
        self._table = table_resource

    def list_all_accounts(self):
        response = self._table.scan()
        sitems = response['Items']
        return sitems

    def list_live_accounts(self):
        response = self._table.scan(FilterExpression = Attr('Active').eq('Y'))
        sitems = response['Items']
        return sitems

    def list_deleted_accounts(self):
        response = self._table.scan(FilterExpression = Attr('Active').eq('N'))
        sitems = response['Items']
        return sitems

    def list_accounts(self, AccountNumber=DEFAULT_ACCOUNTNUMBER):
        response = self._table.query(
            KeyConditionExpression=Key('AccountNumber').eq(AccountNumber)
        )
        sitems = response['Items']
        return sitems

    def add_account(self, accitem ):
        # app.log.debug(f"In add account {accitem}")
        AccountNumber = accitem['AccountNumber']
        response = self._table.get_item(
            Key={'AccountNumber': AccountNumber} )
        if 'Item' in response:
            response = [409, "Conflict, record exists."]
        else:
            response = self._table.put_item(Item=accitem)
        return response

    def get_account(self, AccountNumber):
        response = self._table.get_item(
            Key={'AccountNumber': AccountNumber} )
        if 'Item' in response:
            return [response['Item']]
        else:
            return [404, f"Account {AccountNumber} not found."]

    def delete_account(self, AccountNumber=None):
        response = self._table.delete_item(
            Key={'AccountNumber': AccountNumber} )
        return response

    def update_account(self, accno, accitem):
        response = self._table.get_item(
            Key={'AccountNumber': accno} )

        if 'Item' in response:
            item = response['Item']

            for key in accitem:
                item[key] = accitem[key]

            response = self._table.put_item(Item=item)
        return response

    def toggle_account_active(self, AccountNumber=None, Active=None):
        item = self.get_account(AccountNumber)
        if item[0] != 404:
            item = item[0]
            item['Active'] = Active
            response = self._table.put_item(Item=item)
        else:
            return [404, f"Account {AccountNumber} Not Found"]
        return response
