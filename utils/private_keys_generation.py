
import sys

from bip32utils import BIP32Key
from eth_keys import keys

def get_private_keys(root_private_key, child_id):
    root = BIP32Key.fromExtendedKey(root_private_key)
    eth_private = keys.PrivateKey(root.ChildKey(child_id).k.to_string())
    btc_private = root.ChildKey(child_id).WalletImportFormat()
    return eth_private, btc_private