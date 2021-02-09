import sys
import time
import traceback

from blockchain_common.wrapper_network import WrapperNetwork
from scanner.services.last_block_persister import LastBlockPersister
from scanner.services.scanner import Scanner


class ScannerPolling(Scanner):

    def __init__(self, network: WrapperNetwork, last_block_persister: LastBlockPersister, polling_interval: int,
                 commitment_chain_length: int, reach_interval: int = 0):

        super().__init__(network, last_block_persister)
        self.polling_interval = polling_interval
        self.commitment_chain_length = commitment_chain_length
        self.reach_interval = reach_interval

    def poller(self):
        self.last_block_time = time.time()
        self.next_block_number = self.last_block_persister.get_last_block()
        print('hello from {}'.format(self.network.type), flush=True)
        while True:
            self.polling()

    def polling(self):
        try:
            self.last_block_number = self.network.get_last_block()

            if self.last_block_number - self.next_block_number > self.commitment_chain_length:
                print('{}: Process next block {}/{} immediately.'.format(self.network.type, self.next_block_number,
                                                                         self.last_block_number), flush=True)
                self.load_next_block()
                time.sleep(self.reach_interval)
                return

            time_interval = self.last_block_time - time.time()
            if time_interval > self.WARN_INTERVAL:
                print('{}: there is no block from {} seconds!'.format(self.network.type, time_interval))
            elif time_interval > self.INFO_INTERVAL:
                print('{}: there is no block from {} seconds.'.format(self.network.type, time_interval), flush=True)

            # pending transactions logic

            print('{}: all blocks processed, wait new one.'.format(self.network.type))
        except Exception as e:
            print('{}: exception handled in polling cycle. Continue.'.format(self.network.type))
            print('\n'.join(traceback.format_exception(*sys.exc_info())), flush=True)

        time.sleep(self.polling_interval)

    def load_next_block(self):
        block = self.network.get_block(self.next_block_number)

        self.last_block_persister.save_last_block(self.next_block_number)
        self.next_block_number += 1
        self.last_block_time = time.time()

        self.process_block(block)

    def open(self):
        pass

    def close(self):
        pass
