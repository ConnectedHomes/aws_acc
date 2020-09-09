from uuid import uuid4

from boto3.dynamodb.conditions import Key


DEFAULT_USERNAME = 'default'
# DEFAULT_ACCOUNTNUMBER = '165954058622'
DEFAULT_ACCOUNTNUMBER = '039759963043'
DEFAULT_ACCOUNTNAME = 'AWS Lowes Scale'

class AWSAccDB(object):
    def list_items(self):
        pass

    def add_item(self, description, metadata=None):
        pass

    def get_item(self, uid):
        pass

    def delete_item(self, uid):
        pass

    def update_item(self, uid, description=None, state=None,
                    metadata=None):
        pass


class InMemoryAWSAccDB(AWSAccDB):
    def __init__(self, state=None):
        if state is None:
            state = {}
        self._state = state

    def list_all_items(self):
        all_items = []
        for accno in self._state:
            all_items.extend(self.list_items(accno))
        return all_items

    def list_items(self, accno=DEFAULT_ACCOUNTNAME):
        return self._state.get(username, {}).values()

    def add_item(self, description=None, metadata=None,
                 AccountNumber=DEFAULT_ACCOUNTNUMBER, AccountName=DEFAULT_ACCOUNTNAME):
        if AccountNumber not in self._state:
            self._state[username] = {}
        self._state[AccountNumber][AccountNumber] = {
            'AccountNumber': AccountNumber,
            'Description': description,
            'Active': 'N',
            'metadata': metadata if metadata is not None else {},
            'AccountName': AccountName
        }
        return accno

    def get_item(self, accno):
        return self._state[accname][accno]

    def delete_item(self, accno):
        del self._state[accno]

    def update_item(self, description, metadata=None, state=None,
                    accno=DEFAULT_ACCOUNTNUMBER, accname=DEFAULT_ACCOUNTNAME):
        item = self._state[accno][accname]
        if description is not None:
            item['Description'] = description
        if state is not None:
            item['Active'] = state
        if metadata is not None:
            item['Metadata'] = metadata


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

    def add_item(self, description=None, metadata=None,
                 AccountNumber=DEFAULT_ACCOUNTNUMBER, AccountName=DEFAULT_ACCOUNTNAME):
        self._table.put_item(
            Item={
            'AccountNumber': AccountNumber,
            'Description': description,
            'Active': 'N',
            'metadata': metadata if metadata is not None else {},
            'AccountName': AccountName
        }
        )
        return AccountNumber

    # def add_item(self, description, metadata=None, username=DEFAULT_USERNAME):
    #     uid = str(uuid4())
    #     self._table.put_item(
    #         Item={
    #             'username': username,
    #             'uid': uid,
    #             'description': description,
    #             'state': 'unstarted',
    #             'metadata': metadata if metadata is not None else {},
    #         }
    #     )
    #     return uid

    def get_item(self, accno):
        response = self._table.get_item(
            Key={
                'AccountNumber': accno
            },
        )
        print(response)
        return response['Item']

    def delete_item(self, uid, username=DEFAULT_USERNAME):
        self._table.delete_item(
            Key={
                'username': username,
                'uid': uid,
            }
        )

    def update_item(self, uid, description=None, state=None,
                    metadata=None, username=DEFAULT_USERNAME):
        # We could also use update_item() with an UpdateExpression.
        item = self.get_item(uid, username)
        if description is not None:
            item['description'] = description
        if state is not None:
            item['state'] = state
        if metadata is not None:
            item['metadata'] = metadata
        self._table.put_item(Item=item)
