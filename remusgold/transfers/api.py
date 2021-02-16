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
from remusgold.settings import NETWORK_SETTINGS
from remusgold.account.models import AdvUser
from eth_account import Account

def duc_transfer(duc_address, duc_amount):
    try:
        rpc = DucatuscoreInterface()
        tx_hash = rpc.node_transfer(duc_address, duc_amount)
    except DucatuscoreInterfaceException as err:
        tx_hash = 'ERROR'
        raise APIException(detail=str(err))

    return tx_hash


def confirm_transfer(message):
    tx_hash = message.get('txHash')
    transfer = Transfer.objects.get(tx_hash=tx_hash)
    transfer.transfer_status = 'CONFIRMED'
    transfer.save()


def eth_return_transfer(order, amount, message):
    print('starting eth return', flush = True)
    user=AdvUser.objects.get(id=order.user_id)
    w3= Web3(HTTPProvider(NETWORK_SETTINGS['ETH']['endpoint']))
    print(amount)
    print(w3.eth.gasPrice * GAS_LIMIT * 1.1)
    amount = amount - w3.eth.gasPrice * GAS_LIMIT * 1.1
    to_address = Web3.toChecksumAddress(message['from_address'])
    try:
        tx_params = {
            'nonce': w3.eth.getTransactionCount(Web3.toChecksumAddress(user.eth_address)),  # 'pending'?
            'gasPrice': w3.eth.gasPrice,
            'gas': GAS_LIMIT,
            'to': to_address,
            'value': int(amount),
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
        return repr(e)

def usdc_return_transfer():
    #w3= Web3(HTTPProvider(NETWORK_SETTINGS['ETH']['endpoint']))
    pass

def btc_return_transfer():
    #w3= Web3(HTTPProvider(NETWORK_SETTINGS['ETH']['endpoint']))
    pass