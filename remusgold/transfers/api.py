from remusgold.transfers.models import Transfer
import json
import requests
from django.utils import timezone
from decimal import Decimal
from remusgold.litecoin_rpc import DucatuscoreInterface, DucatuscoreInterfaceException
from rest_framework.exceptions import PermissionDenied, APIException
from remusgold.settings import RATES_API_URL
from remusgold.consts import DECIMALS
from web3 import Web3, HTTPProvider
from web3.exceptions import TransactionNotFound
from remusgold.settings import GAS_LIMIT
from remusgold.settings import ROOT_KEYS
from utils.private_keys_generation import get_private_keys


def eth_return_transfer(order, amount, message):
    print('starting eth return', flush = True)
    w3= Web3(HTTPProvider(NETWORK_SETTINGS['ETH']['endpoint']))
    amount = amount - w3.eth.gasPrice * GAS_LIMIT * 1.1
    to_address = message['from_address']
    try:
        tx_params = {
            'nonce': w3.eth.getTransactionCount(order.eth_address),  # 'pending'?
            'gasPrice': w3.eth.gasPrice,
            'gas': GAS_LIMIT,
            'to': to_address,
            'value': amount,
            'data': b'',
        }
        root_private_key = ROOT_KEYS['mainnet']['private']
        root_public_key = ROOT_KEYS['mainnet']['public']
        eth_priv_key, btc_priv_key = get_private_keys(root_private_key, order.user_id)
        signed = w3.eth.account.signTransaction(tx_params, eth_priv_key)
        tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_hex = tx_hash.hex()
        print(f'eth return for {amount} {order.currency} to {to_address} ok, tx hash:{tx_hex}\n', flush=True)
        return tx_hex
    except Exception as e:
        print(e)
        transfer.tx_error = repr(e)
        transfer.state = 'FAIL'
        transfer.save()
        return None

def usdc_return_transfer():
    #w3= Web3(HTTPProvider(NETWORK_SETTINGS['ETH']['endpoint']))
    pass

def btc_return_transfer():
    #w3= Web3(HTTPProvider(NETWORK_SETTINGS['ETH']['endpoint']))
    pass