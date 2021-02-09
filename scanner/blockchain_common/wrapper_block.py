import typing

from blockchain_common.wrapper_transaction import WrapperTransaction

class WrapperBlock:
    def __init__(self, hash: str, number: int, timestamp: int, transactions: typing.List[WrapperTransaction]):
        self.hash = hash
        self.number = number
        self.timestamp = timestamp
        self.transactions = transactions
