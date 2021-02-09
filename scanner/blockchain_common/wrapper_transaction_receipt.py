import typing


class WrapperTransactionReceipt:
    def __init__(self, tx_hash: str, contracts: typing.List[str], logs: str, success: bool):
        self.tx_hash = tx_hash
        self.contracts = contracts
        self.logs = logs
        self.success = success
