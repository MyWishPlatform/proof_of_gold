import typing

from blockchain_common.wrapper_output import WrapperOutput


class WrapperTransaction:

    def __init__(self, tx_hash: str, inputs: typing.List[str], outputs: typing.List[WrapperOutput],
                 contract_creation: bool, creates:str):
        self.tx_hash = tx_hash
        self.inputs = inputs
        self.outputs = outputs
        self.contract_creation = contract_creation
        self.creates = creates
