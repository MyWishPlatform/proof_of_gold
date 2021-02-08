from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from http.client import RemoteDisconnected
from decimal import Decimal

from remusgold.settings import NETWORK_SETTINGS
from remusgold.consts import DECIMALS


def retry_on_http_disconnection(req):
    def wrapper(*args, **kwargs):
        for attempt in range(10):
            print('attempt', attempt, flush=True)
            try:
                return req(*args, **kwargs)
            except RemoteDisconnected as e:
                print(e, flush=True)
                rpc_response = False
            if not isinstance(rpc_response, bool):
                print(rpc_response, flush=True)
                break
        else:
            raise DucatuscoreInterfaceException('cannot get unspent with 10 attempts')

    return wrapper


class DucatuscoreInterfaceException(Exception):
    pass


class DucatuscoreInterface:
    endpoint = None
    settings = None

    def __init__(self):

        self.settings = NETWORK_SETTINGS['DUC']
        self.setup_endpoint()
        self.rpc = AuthServiceProxy(self.endpoint)
        self.check_connection()

    def setup_endpoint(self):
        self.endpoint = 'http://{user}:{pwd}@{host}:{port}'.format(
            user=self.settings['user'],
            pwd=self.settings['password'],
            host=self.settings['host'],
            port=self.settings['port']
        )
        return

    def check_connection(self):
        block = self.rpc.getblockcount()
        if block and block > 0:
            return True
        else:
            raise DucatuscoreInterfaceException('Ducatus node not connected')

    @retry_on_http_disconnection
    def node_transfer(self, address, amount):
        try:
            value = amount / DECIMALS['DUC']
            print('try sending {value} DUC to {addr}'.format(value=value, addr=address), flush=True)
            self.rpc.walletpassphrase(self.settings['wallet_password'], 30)
            res = self.rpc.sendtoaddress(address, value)
            print(res, flush=True)
            return res
        except JSONRPCException as e:
            err = 'DUCATUS TRANSFER ERROR: transfer for {amount} DUC for {addr} failed' \
                .format(amount=amount, addr=address)
            print(err, flush=True)
            print(e, flush=True)
            raise DucatuscoreInterfaceException(err + '\n' + str(e))