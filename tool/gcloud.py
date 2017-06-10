import gcloud
from gcloud import datastore

client = gcloud.datastore.Client('g-action')


data = [
            {
                'username': 'john',
                'portfolio':
                {
                    'cash': [
                         {'account_id': 123, 'account_name': 'account 1','balance': 1000000, 'currency': 'EUR'},
                         {'account_id': 456, 'account_name': 'account 2', 'balance': 2000000, 'currency': 'USD'}],
                    'asset': [
                        {'asset': 'fx', 'mtm': 200000},
                        {'asset': 'equity', 'mtm': 200000},
                        {'asset': 'fund', 'mtm': 200000}]
                    }
            }
        ]

for d in data:
    parent_key = client.key('Users', d['username'])
    entity_user = datastore.Entity(parent_key)
    client.put(entity_user)
    
    account = datastore.Entity(client.key('Account', parent=parent_key))
    account.update(d['portfolio']['cash'])
