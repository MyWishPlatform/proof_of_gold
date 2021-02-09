from bitcoinrpc.authproxy import AuthServiceProxy

from settings.settings_local import NETWORKS, DECIMALS


class BTCInterfaceException(Exception):
    pass


class BTCInterface:
    endpoint = None
    settings = None

    def __init__(self, net_type):

        self.settings = NETWORKS[net_type]
        self.decimal = DECIMALS['BTC']
        self.setup_endpoint()
        self._rpc = AuthServiceProxy
        self.check_connection()

    @property
    def rpc(self):
        return self._rpc(self.endpoint)

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
            raise Exception('Ducatus node not connected')

    def dec_to_int(self, value):
        return int(value * self.decimal)
