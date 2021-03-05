
import time
import requests
from bitcoinrpc.authproxy import AuthServiceProxy

from remusgold.settings import NETWORK_SETTINGS
from remusgold.consts import DECIMALS


class BitcoinRPC:
    def __init__(self):
        self.connection = None
        self.network_info = None
        self.version = None
        self.relay_fee = None
        self.establish_connection()

    def establish_connection(self):
        self.connection = AuthServiceProxy(NETWORK_SETTINGS['BTC']['endpoint'])
        self.network_info = self.connection.getnetworkinfo()
        self.version = int(str(self.network_info['version'])[:2])
        self.relay_fee = int(self.network_info['relayfee'] * DECIMALS['BTC'])

    def reconnect(self):
        self.establish_connection()

    def create_raw_transaction(self, input_params, output_params):
        self.reconnect()
        return self.connection.createrawtransaction(input_params, output_params)

    def sign_raw_transaction(self, tx, private_key):
        self.reconnect()
        if self.version >= 17:
            return self.connection.signrawtransactionwithkey(tx, [private_key])
        else:
            return self.connection.signrawtransaction(tx, None, [private_key])

    def send_raw_transaction(self, tx_hex):
        self.reconnect()
        return self.connection.sendrawtransaction(tx_hex)

    def construct_and_send_tx(self, input_params, output_params, private_key):
        tx = self.create_raw_transaction(input_params, output_params)

        signed = self.sign_raw_transaction(tx, private_key)

        try:
            tx_hash = self.send_raw_transaction(signed['hex'])
            print('tx', tx_hash, flush=True)
            return tx_hash
        except Exception as e:
            print('FAILED SENDING TRANSACTION', flush=True)
            print(e, flush=True)
            return None


class BitcoinAPI:
    def __init__(self):
        self.network = 'testnet'
        if 'production' in NETWORK_SETTINGS['BTC']:
            if NETWORK_SETTINGS['BTC']['production']:
                self.network = 'mainnet'

        self.base_url = None
        self.set_base_url()

    def set_base_url(self):
        self.base_url = f'https://api.bitcore.io/api/BTC/{self.network}'

    def get_address_response(self, address):
        endpoint_url = f'{self.base_url}/address/{address}'
        res = requests.get(endpoint_url)
        if not res.ok:
            return [], False
        else:
            valid_json = len(res.json()) > 0
            if not valid_json:
                print('Address have no transactions and balance is 0', flush=True)
                return [], True

            return res.json(), True

    def get_address_unspent_all(self, address):
        inputs_of_address, response_ok = self.get_address_response(address)
        if not response_ok:
            return [], 0, False

        if response_ok and len(inputs_of_address) == 0:
            return inputs_of_address, 0, True

        inputs_value = 0
        unspent_inputs = []
        for input_tx in inputs_of_address:
            if not input_tx['spentTxid']:
                unspent_inputs.append({
                    'txid': input_tx['mintTxid'],
                    'vout': input_tx['mintIndex']
                })
                inputs_value += input_tx['value']

        return unspent_inputs, inputs_value, True

    def get_address_unspent_from_tx(self, address, tx_hash):
        inputs_of_address, response_ok = self.get_address_response(address)
        if not response_ok:
            return [], 0, False

        if response_ok and len(inputs_of_address) == 0:
            return inputs_of_address, 0, True

        # find vout
        vout = None
        input_value = 0
        for input_tx in inputs_of_address:
            if not input_tx['spentTxid'] and input_tx['mintTxid'] == tx_hash:
                vout = input_tx['mintIndex']
                input_value = input_tx['value']

        if vout is None:
            return [], 0, False

        input_params = [{'txid': tx_hash, 'vout': vout}]
        return input_params, input_value, True

    def get_return_address(self, tx_hash):
        endpoint_url = f'{self.base_url}/tx/{tx_hash}/coins'
        res = requests.get(endpoint_url)
        if not res.ok:
            return '', False
        else:
            tx_info = res.json()

        inputs_of_tx = tx_info['inputs']
        if len(inputs_of_tx) == 0:
            return '', False

        first_input = inputs_of_tx[0]
        return_address = first_input['address']

        address_found = False
        if return_address:
            address_found = True

        return return_address, address_found
