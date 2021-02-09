import os

from blockchain_common.wrapper_network import WrapperNetwork


class LastBlockPersister:
    # TODO move into database
    base_dir = 'settings'

    def __init__(self, network: WrapperNetwork):
        self.network_name: str = network.type

    def get_last_block(self) -> int:
        try:
            with open(os.path.join(self.base_dir, self.network_name), 'r') as file:
                last_block_number = file.read()
        except FileNotFoundError:
            return 1
        return int(last_block_number)

    def save_last_block(self, last_block_number: int):
        with open(os.path.join(self.base_dir, self.network_name), 'w') as file:
            file.write(str(last_block_number))
