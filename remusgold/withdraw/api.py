import requests
import time
import collections
from web3 import Web3, HTTPProvider
from web3.exceptions import TransactionNotFound
from eth_account import Account

from remusgold.account.models import AdvUser
from remusgold.settings import NETWORK_SETTINGS, ROOT_KEYS, USDC_CONTRACT
from utils.private_keys_generation import get_private_keys
from remusgold.consts import DECIMALS
from remusgold.bitcoin_api import BitcoinRPC, BitcoinAPI
from remusgold.rates.models import UsdRate


def withdraw_funds():
    '''
    Withdrawing funds. Executed by withdraw_funds command in manage.py
    '''
    withdraw_parameters = {
        'root_private_key': ROOT_KEYS['mainnet']['private'],
        'root_public_key': ROOT_KEYS['mainnet']['public'],
        'btc_testnet_root_private_key': ROOT_KEYS['testnet']['private'],
        'btc_testnet_root_public_key': ROOT_KEYS['testnet']['public'],

        'address_to_btc': NETWORK_SETTINGS['BTC']['address'],
        'address_to_eth': NETWORK_SETTINGS['ETH']['address'],
        'gas_priv_key': NETWORK_SETTINGS['ETH']['private'],
    }

    for key, value in withdraw_parameters.items():
        if not value:
            print(f'Value not found for parameter {key}. Aborting', flush=True)
            return

    all_users = AdvUser.objects.all().exclude(eth_address=None, btc_address=None)
    usdt_gas_transactions = collections.defaultdict(list)
    delayed_transactions_addresses = []

    print('BTC WITHDRAW', flush=True)
    for user in all_users:
        eth_priv_key, btc_priv_key = get_private_keys(withdraw_parameters['root_private_key'], user.id)
        if NETWORK_SETTINGS['BTC']['testnet']:
            garbage_eth, btc_priv_key = get_private_keys(withdraw_parameters['btc_testnet_root_private_key'], user.id)
        print(f'BTC address: {user.btc_address}', flush=True)
        try:
            process_withdraw_btc(withdraw_parameters, user, btc_priv_key)
        except Exception as e:
            print('BTC withdraw failed. Error is:', flush=True)
            print(e, flush=True)

    print('USDT WITHDRAW (sending gas)', flush=True)
    for user in all_users:
        eth_priv_key, btc_priv_key = get_private_keys(withdraw_parameters['root_private_key'], user.id)
        print(f'ETH address: {user.eth_address}', flush=True)
        try:
            process_send_gas_for_usdt(withdraw_parameters, user, eth_priv_key, usdt_gas_transactions)
        except Exception as e:
            print('USDT sending gas failed. Error is:', flush=True)
            print(e, flush=True)

    print('USDT WITHDRAW (sending tokens)', flush=True)
    try:
        parse_usdt_transactions(usdt_gas_transactions, delayed_transactions_addresses)
    except Exception as e:
        print('USDT transaction sending failed. Error is:', flush=True)
        print(e, flush=True)

    print('Waiting 7 minutes because USDT transactions affect ETH balance')
    time.sleep(7 * 60)

    print('ETH WITHDRAW', flush=True)
    for user in all_users:
        eth_priv_key, btc_priv_key = get_private_keys(withdraw_parameters['root_private_key'], user.id)
        print(f'ETH address: {user.eth_address}', flush=True)
        if user.eth_address in delayed_transactions_addresses:
            print('address {} skipped because of delayed gas transaction'.format(account.eth_address), flush=True)
            continue
        try:
            process_withdraw_eth(withdraw_parameters, user, eth_priv_key)
        except Exception as e:
            print('ETH withdraw failed. Error is:', flush=True)
            print(e, flush=True)


def normalize_gas_price(gas_price):
    gwei_decimals = 10 ** 9
    gas = int(round(gas_price / gwei_decimals, 0)) * gwei_decimals
    lower_gas = gas - 1 if gas > 2 else gas
    return gas, lower_gas


def check_tx_success(tx):
    web3 = Web3(HTTPProvider(NETWORK_SETTINGS['ETH']['endpoint']))
    try:
        receipt = web3.eth.getTransactionReceipt(tx)
        if receipt['status'] == 1:
            return True
        else:
            return False
    except TransactionNotFound:
        return False


def check_tx(tx):
    print(f'Checking transaction {tx} until found in network', flush=True)
    tx_found = check_tx_success(tx)
    if tx_found:
        print(f'Ok, found transaction {tx} and it was completed', flush=True)
        return True


def process_withdraw_eth(params, account, priv_key):
    web3 = Web3(HTTPProvider(NETWORK_SETTINGS['ETH']['endpoint']))

    gas_limit = 21000
    gas_price, fake_gas_price = normalize_gas_price(web3.eth.gasPrice)
    total_gas_fee = gas_price * gas_limit

    from_address = account.eth_address
    to_address = params['address_to_eth']

    balance = web3.eth.getBalance(web3.toChecksumAddress(from_address), 'pending')
    nonce = web3.eth.getTransactionCount(web3.toChecksumAddress(from_address), 'pending')

    if balance < total_gas_fee:
        print(f'Address {from_address} skipped: balance {balance} < tx fee of {total_gas_fee}', flush=True)
        return

    withdraw_amount = int(balance) - total_gas_fee

    tx_params = {
        'chainId': web3.eth.chainId,
        'gas': gas_limit,
        'nonce': nonce,
        'gasPrice': fake_gas_price,
        'to': web3.toChecksumAddress(params['address_to_eth']),
        'value': int(withdraw_amount)
    }

    print(f'Withdraw tx params: from {from_address} to {to_address} on amount {withdraw_amount}', flush=True)

    signed_tx = Account.signTransaction(tx_params, priv_key)
    print('signed tx:', signed_tx, flush=True)
    print('raw tx:', signed_tx['rawTransaction'].hex(), flush=True)
    try:
        sent_tx = web3.eth.sendRawTransaction(signed_tx['rawTransaction'])
        print(f'sent tx: {sent_tx.hex()}', flush=True)
    except Exception as e:
        err_str = f'Refund failed for address {from_address} and amount {withdraw_amount} ({balance} - {total_gas_fee})'
        print(err_str, flush=True)
        print(e, flush=True)
    return


def process_send_gas_for_usdt(params, account, priv_key, transactions):
    web3 = Web3(HTTPProvider(NETWORK_SETTINGS['ETH']['endpoint']))
    myContract = web3.eth.contract(
        address=web3.toChecksumAddress(USDC_CONTRACT['address']), abi=USDC_CONTRACT['abi']
    )

    gas_limit = 21000
    erc20_gas_limit = 200000
    gas_price, fake_gas_price = normalize_gas_price(web3.eth.gasPrice)
    erc20_gas_price, erc20_fake_gas_price = normalize_gas_price(web3.eth.gasPrice)
    total_gas_fee = gas_price * gas_limit
    erc20_gas_fee = erc20_gas_price * erc20_gas_limit
    rate = UsdRate.objects.get(currency='ETH')
    rate = rate.rate
    from_address = account.eth_address
    to_address = params['address_to_eth']

    balance = myContract.functions.balanceOf(web3.toChecksumAddress(from_address)).call()  # / ETH/USDTCourse
    balance_check = int((float(balance) / float(DECIMALS['USDC']) / float(rate)) * float(DECIMALS['ETH']))
    ETH_balance = web3.eth.getBalance(web3.toChecksumAddress(from_address))
    nonce = web3.eth.getTransactionCount(web3.toChecksumAddress(from_address), 'pending')
    gas_nonce = web3.eth.getTransactionCount(
        web3.toChecksumAddress(NETWORK_SETTINGS['ETH']['address']), 'pending')
    if balance_check <= (total_gas_fee + erc20_gas_fee):
        print(f'Address {from_address} skipped: balance {balance_check} < tx fee of {total_gas_fee + erc20_gas_fee}',
              flush=True)
        return

    withdraw_amount = int(balance)

    tx_params = {
        'chainId': web3.eth.chainId,
        'gas': erc20_gas_limit,
        'nonce': nonce,
        'gasPrice': erc20_fake_gas_price,
        'from': web3.toChecksumAddress(from_address),
        'to': web3.toChecksumAddress(params['address_to_eth']),
        'value': int(withdraw_amount),
        'priv_key': priv_key
    }

    gas_tx_params = {
        'chainId': web3.eth.chainId,
        'gas': gas_limit,
        'nonce': gas_nonce,
        'gasPrice': fake_gas_price,
        'to': web3.toChecksumAddress(from_address),
        'value': int(erc20_gas_fee * 1.2)
    }

    if ETH_balance > int(erc20_gas_fee * 1.1):
        print('Enough balance {} > {} for withdrawing {} from {}'.format(ETH_balance, int(erc20_gas_fee * 1.1), balance,
                                                                         from_address), flush=True)
        process_withdraw_usdt([tx_params])
        return

    print(f'send gas to {from_address}', flush=True)

    signed_tx = Account.signTransaction(gas_tx_params, params['gas_priv_key'])
    try:
        sent_tx = web3.eth.sendRawTransaction(signed_tx['rawTransaction'])
        print(f'sent tx: {sent_tx.hex()}', flush=True)
        transactions[sent_tx.hex()].append(tx_params)
    except Exception as e:
        err_str = f'Refund failed for address {from_address} and amount {withdraw_amount} ({balance} - {total_gas_fee})'
        print(err_str, flush=True)
        print(e, flush=True)


def process_withdraw_usdt(tx_params):
    web3 = Web3(HTTPProvider(NETWORK_SETTINGS['ETH']['endpoint']))
    myContract = web3.eth.contract(
        address=web3.toChecksumAddress(USDC_CONTRACT['address']), abi=USDC_CONTRACT['abi'])

    priv_key = tx_params[0]['priv_key']
    from_address = tx_params[0]['from']
    to_address = tx_params[0]['to']
    value = tx_params[0]['value']
    del tx_params[0]['priv_key']
    del tx_params[0]['from']
    del tx_params[0]['to']
    del tx_params[0]['value']
    del tx_params[0]['chainId']

    print('Withdraw tx params: from {} to {} on amount {}'.format(from_address, to_address, value), flush=True)
    initial_tx = myContract.functions.transfer(to_address, value).buildTransaction(tx_params[0])
    signed_tx = Account.signTransaction(initial_tx, priv_key)
    print('signed tx:', signed_tx, flush=True)
    print('raw tx:', signed_tx['rawTransaction'].hex(), flush=True)
    try:
        sent_tx = web3.eth.sendRawTransaction(signed_tx['rawTransaction'])
        print(f'sent tx: {sent_tx.hex()}', flush=True)
    except Exception as e:
        err_str = 'Refund failed for address {} and amount {})'.format(from_address, value)
        print(err_str, flush=True)
        print(e, flush=True)
    return


def parse_usdt_transactions(transactions, delayed_transactions_addresses):
    count = 0
    while transactions:
        if count >= 42:
            print(
                'Transaction receipts not found in 7 minutes. Supposedly they are still in pending state due to high transaction' +
                'traffic or they failed, please check hashs {} on Etherscan'.format(transactions.keys()),
                flush=True)
            break
        to_del = []
        for transaction in transactions.keys():
            if check_tx(transaction):
                process_withdraw_usdt(transactions[transaction])
                to_del.append(transaction)
                continue
        for transaction in to_del:
            transactions.pop(transaction)
        time.sleep(10)
        count += 1
    for transaction in transactions:
        delayed_transactions_addresses.append(transactions[transaction][0]['from'].lower())


def process_withdraw_btc(params, account, priv_key):
    if isinstance(account, str):
        from_address = account
    else:
        from_address = account.btc_address

    to_address = params['address_to_btc']

    api = BitcoinAPI()
    inputs, value, response_ok = api.get_address_unspent_all(from_address)

    if not response_ok:
        print(f'Failed to fetch information about BTC address {from_address}', flush=True)
        return

    balance = int(value)
    if balance <= 0:
        balance = 0

    rpc = BitcoinRPC()
    transaction_fee = rpc.relay_fee
    if balance < transaction_fee:
        print(f'Address skipped: {from_address}: balance {balance} < tx fee of {transaction_fee}', flush=True)
        return

    withdraw_amount = (balance - transaction_fee) / DECIMALS['BTC']

    output_params = {to_address: withdraw_amount}

    print(f'Withdraw tx params: from {from_address} to {to_address} on amount {withdraw_amount}', flush=True)
    print('input_params', inputs, flush=True)
    print('output_params', output_params, flush=True)

    sent_tx_hash = rpc.construct_and_send_tx(inputs, output_params, priv_key)

    if not sent_tx_hash:
        err_str = f'Withdraw failed for address {from_address} and amount {withdraw_amount} ({balance} - {transaction_fee})'
        print(err_str, flush=True)

    return
