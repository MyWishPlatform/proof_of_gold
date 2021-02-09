from bitcoinrpc.authproxy import JSONRPCException

from blockchain_common.btc_rpc import BTCInterface
from blockchain_common.wrapper_block import WrapperBlock
from blockchain_common.wrapper_network import WrapperNetwork
from blockchain_common.wrapper_output import WrapperOutput
from blockchain_common.wrapper_transaction import WrapperTransaction


class BTCNetwork(WrapperNetwork):

    ignore_output_types = ['nulldata', 'nonstandard']

    def __init__(self, net_type: str):
        super().__init__(net_type)
        self.interface = BTCInterface(net_type)

    def get_last_block(self):
        return self.interface.rpc.getblockcount()

    def get_block(self, number: int) -> WrapperBlock:
        block_hash = self.interface.rpc.getblockhash(number)

        # For BTC we can obtain block with filled tx objects,
        # but some rpc don't support this, and we need to obtain all tx manually
        try:
            block = self.interface.rpc.getblock(block_hash, 2)
        except JSONRPCException:
            block = self.interface.rpc.getblock(block_hash, True)
            block['tx'] = [self.interface.rpc.getrawtransaction(t, 1) for t in block['tx']]

        transactions = [WrapperTransaction(
            t['txid'],
            [i for i in t['vin']],
            self._build_outputs(t),
            False,
            ""
        ) for t in block['tx']]

        wb = WrapperBlock(
            block['hash'],
            block['height'],
            block['time'],
            transactions
        )
        return wb

    def _build_outputs(self, tx) -> [WrapperOutput]:
        vout = tx['vout']
        return [WrapperOutput(
            tx['hash'],
            o['n'],
            o['scriptPubKey']['addresses'],
            self.interface.dec_to_int(o['value']),
            None
        ) for o in vout if o['scriptPubKey']['type'] not in self.ignore_output_types]
