class WrapperOutput:
    def __init__(self, parent_transaction: str, index: int, address: str, value: int, raw_output_script):
        self.parent_transaction = parent_transaction
        self.index = index
        self.address = address
        self.value = value
        self.raw_output_script = raw_output_script
