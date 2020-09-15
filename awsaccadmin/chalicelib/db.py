from uuid import uuid4
from boto3.dynamodb.conditions import Key

DEFAULT_ACCOUNTNUMBER = '039759963043'

class AWSAccDB(object):
    def list_items(self):
        pass

    def add_item(self, accitem):
        pass

    def get_item(self, AccountNumber):
        pass

    def delete_item(self, AccountNumber):
        pass

    def update_item(self, AccountNumber, jsonbody):
        pass


class DynamoDBAWSAcc(AWSAccDB):
    def __init__(self, table_resource):
        self._table = table_resource

    def list_all_items(self):
        response = self._table.scan()
        return response['Items']

    def list_items(self, AccountNumber=DEFAULT_ACCOUNTNUMBER):
        response = self._table.query(
            KeyConditionExpression=Key('AccountNumber').eq(AccountNumber)
        )
        return response['Items']

    def add_item(self, accitem ):
        response = self._table.put_item(Item=accitem)
        return response

    def get_item(self, AccountNumber):
        response = self._table.get_item(
            Key={'AccountNumber': AccountNumber} )
        if 'Item' in response:
            return response['Item']
        else:
            return f"Account {AccountNumber} not found."

    def delete_item(self, AccountNumber=None):
        response = self._table.delete_item(
            Key={'AccountNumber': AccountNumber} )
        return response

    def update_item(self, AccountNumber, jsonbody):
        item = self.get_item(AccountNumber)
        for key in jsonbody:
            item[key] = jsonbody[key]
        response = self._table.put_item(Item=item)
        return response
