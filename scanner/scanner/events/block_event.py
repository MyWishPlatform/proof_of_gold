import typing

from blockchain_common.wrapper_block import WrapperBlock
from blockchain_common.wrapper_transaction import WrapperTransaction
from blockchain_common.wrapper_network import WrapperNetwork


class BlockEvent:
    def __init__(self, network: WrapperNetwork, block: WrapperBlock,
                 transactions_by_address: typing.Dict[str, typing.List[WrapperTransaction]]):
        self.network = network
        self.block = block
        self.transactions_by_address = transactions_by_address
