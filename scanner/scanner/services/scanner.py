from blockchain_common.wrapper_network import WrapperNetwork
from scanner.services.last_block_persister import LastBlockPersister


class Scanner:
    INFO_INTERVAL = 60000
    WARN_INTERVAL = 120000

    def __init__(self, network: WrapperNetwork, last_block_persister: LastBlockPersister):
        self.network = network
        self.last_block_persister = last_block_persister

    def process_block(self, block):
        pass
    #
    # def set_worker(self):
    #     pass
    #
    # def onApplicationLoaded(self):
    #     pass
    #
    # def onApplicationClosed(self):
    #     pass
    #
    # def open(self):
    #     pass
    #
    # def close(self):
    #     pass
