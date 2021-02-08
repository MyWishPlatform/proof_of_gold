import binascii
import requests

from remusgold.settings import ROOT_KEYS, BITCOIN_URLS, IS_TESTNET_PAYMENTS

def get_root_key():
    network = 'mainnet'

    if IS_TESTNET_PAYMENTS:
        network = 'testnet'

    root_pub_key = ROOT_KEYS[network]['public']

    return root_pub_key