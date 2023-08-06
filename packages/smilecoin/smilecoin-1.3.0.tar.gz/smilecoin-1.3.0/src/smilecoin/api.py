from algosdk.encoding import future_msgpack_decode

import requests

import json

documentation_link = 'https://docs.smilecoin.us'

class API:
    def __init__(self):
        self.api_key = None
        self.smile_price = requests.get('https://api.smilecoin.us/api/v1/smile/price').json()['price']
        self.environ = 'testnet'

    def auth(self, api_key):
        self.api_key = api_key

    def verify_txn(self, amount, txn):
        try:
            txn = future_msgpack_decode(txn).transaction
            # TODO: look up intended recipient address based on self.api_key
            platform_address = ''

            receiver, txn_amount = txn.receiver, txn.amount / 1000000

            txn_amount /= self.smile_price()
            if platform_address != receiver or amount != txn_amount:
                return False
            return True
        except Exception:
            return False

    def receive(self, txn):
        try:
            if self.api_key is None:
                return {'status_code': 400, 'message': 'You must authorize your request first!  See documentation {}/accept-payments#2.-create-transaction.'.format(documentation_link)}

            headers = {'api-key': self.api_key, 'Content-type': 'application/json'}

            if not isinstance(txn, dict): return {'message': 'You must pass a dictionary!'}

            if self.environ == 'mainnet': r = requests.post('https://api.smilecoin.us/api/v1/smile/receive', headers=headers, json=txn)
            else: r = requests.post('https://api.smilecoin.dev/api/v1/smile/receive', headers=headers, json=txn)

            response = json.loads(r.content)

            if r.status_code != 201:
                message = 'Could not complete receive because {}.  Visit {}/receive-payments#3.-send-transaction for help.'.format(response, documentation_link)
                return {'status_code': r.status_code, 'message': message}

            return {'status_code': r.status_code, 'usd_amount': response['usd_amount'], 'message': response['message'], 'txn_id': response['txn_id']}
        except Exception as e:
            return {'status_code': 500, 'usd_amount': None, 'message': 'Receive method failed because {}'.format(e), 'txn_id': None}


    def send(self, txn):
        try:
            if self.api_key is None:
                return {'status_code': 400, 'message': 'You must authorize your request first!  See documentation {}/accept-payments#2.-create-transaction.'.format(documentation_link)}

            headers = {'api-key': self.api_key, 'Content-type': 'application/json'}

            if not isinstance(txn, dict): return {'message': 'You must pass a dictionary!'}

            if self.environ == 'mainnet': r = requests.post('https://api.smilecoin.us/api/v1/smile/send', headers=headers, json=txn)
            else: r = requests.post('https://api.smilecoin.dev/api/v1/smile/send', headers=headers, json=txn)

            response = json.loads(r.content)

            if r.status_code != 201:
                message = 'Could not complete send because {}.  Visit {}/send-payments#4.-complete-transaction for help.'.format(response, documentation_link)
                return {'status_code': r.status_code, 'message': message}

            return {'status_code': r.status_code, 'usd_amount': response['usd_amount'], 'message': response['message']}

        except Exception as e:
            return {'status_code': 500, 'usd_amount': None, 'message': 'Send method failed because {}'.format(e)}