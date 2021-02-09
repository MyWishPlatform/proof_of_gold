from collections import defaultdict

from eventscanner.queue.subscribers import pub

from scanner.events.block_event import BlockEvent
from scanner.services.scanner_polling import ScannerPolling


class BTCScanner(ScannerPolling):
    def process_block(self, block):
        print('{}: new block received {} ({})'.format(self.network.type, block.number, block.hash), flush=True)
        if not block.transactions:
            print('{}: no transactions in {} ({})'.format(self.network.type, block.number, block.hash), flush=True)
            return

        address_transactions = defaultdict(list)
        for transaction in block.transactions:
            for output in transaction.outputs:
                for a in output.address:
                    address_transactions[a].append(transaction)

        print('{}: transactions'.format(self.network.type), address_transactions, flush=True)
        block_event = BlockEvent(self.network, block, address_transactions)

        pub.sendMessage(self.network.type, block_event=block_event)
