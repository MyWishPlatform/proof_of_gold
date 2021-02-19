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
from remusgold.settings import GAS_LIMIT, ERC20_GAS_LIMIT
from remusgold.settings import ROOT_KEYS
from utils.private_keys_generation import get_private_keys
from remusgold.settings import NETWORK_SETTINGS, USDC_CONTRACT
from remusgold.account.models import AdvUser
from eth_account import Account
from remusgold.bitcoin_api import BitcoinAPI, BitcoinRPC

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

def usdc_return_transfer(order, amount, message):
    print('starting USDC return', flush=True)
    user = AdvUser.objects.get(id=order.user_id)
    w3 = Web3(HTTPProvider(NETWORK_SETTINGS['ETH']['endpoint']))
    myContract = w3.eth.contract(address=Web3.toChecksumAddress(USDC_CONTRACT['address']), abi=USDC_CONTRACT['abi'])
    print(amount)
    to_address = Web3.toChecksumAddress(message['from_address'])
    try:
        tx_params = {
            'nonce': w3.eth.getTransactionCount(Web3.toChecksumAddress(user.eth_address)),  # 'pending'?
            'gasPrice': w3.eth.gasPrice,
            'gas': ERC20_GAS_LIMIT,
        }
        root_private_key = ROOT_KEYS['mainnet']['private']
        root_public_key = ROOT_KEYS['mainnet']['public']
        eth_priv_key, btc_priv_key = get_private_keys(root_private_key, order.user_id)
        initial_tx = myContract.functions.transfer(to_address, int(amount)).buildTransaction(tx_params)
        signed = Account.signTransaction(initial_tx, eth_priv_key)
        tx_hash = w3.eth.sendRawTransaction(signed['rawTransaction'])
        tx_hex = tx_hash.hex()
        print(f'eth return for {amount} {order.currency} to {to_address} ok, tx hash:{tx_hex}\n', flush=True)
        return tx_hex
    except Exception as e:
        print(e)
        return repr(e)

def btc_return_transfer(order, amount, message):
    api = BitcoinAPI()
    return_address, ok_response = api.get_return_address(message['transactionHash'])
    if not ok_response:
        print('BTC REFUND FAILED: Cannot get return address', flush=True)
        print('tx hash', tx_hash, flush=True)
        return

    user = AdvUser.objects.get(id=order.user_id)
    root_private_key = (ROOT_KEYS['testnet']['private'] if NETWORK_SETTINGS['BTC']['testnet'] else ROOT_KEYS['mainnet']['private'])
    eth, priv = get_private_keys(root_private_key, user.id)
    address_from = user.btc_address
    tx_hash = message['transactionHash']
    print(f'Creating refund for {tx_hash} at {amount} from {address_from} to {return_address}', flush=True)

    input_params, input_value, ok_response = api.get_address_unspent_from_tx(address_from, tx_hash)
    if not ok_response:
        print('BTC REFUND FAILED: Cannot found vout for transaction', flush=True)
        return

    if ok_response and len(input_params) == 0:
        # it's already in bitcoin_api as response with zero balance
        return

    print('found unspent input:', input_params, flush=True)

    rpc = BitcoinRPC()
    network_fee = rpc.relay_fee
    raw_return_amount = int(amount) - network_fee
    return_amount = raw_return_amount / DECIMALS['BTC']

    output_params = {return_address: return_amount}
    if int(amount) < int(input_value):
        raw_change_amount = int(input_value) - raw_return_amount - network_fee
        change_amount = raw_change_amount / DECIMALS['BTC']
        output_params[address_from] = change_amount

    print(f'Refund tx params: from {address_from} to {return_address} on amount {return_amount}', flush=True)
    print('input_params', input_params, flush=True)
    print('output_params', output_params, flush=True)

    sent_tx = rpc.construct_and_send_tx(input_params, output_params, priv)

    if not sent_tx:
        err_str = f'Refund failed for address {address_from} and amount {return_amount} ({amount} - {network_fee})'
        print(err_str, flush=True)

    return sent_tx