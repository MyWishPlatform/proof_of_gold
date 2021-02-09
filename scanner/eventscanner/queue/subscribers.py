from pubsub import pub

from eventscanner.monitors.payments import (BTCPaymentMonitor,
                                            DucPaymentMonitor,
                                            EthPaymentMonitor,
                                            DucxPaymentMonitor,
                                            ERC20PaymentMonitor)
from eventscanner.monitors import transfer

pub.subscribe(BTCPaymentMonitor.on_new_block_event, 'BTC_MAINNET')
pub.subscribe(ERC20PaymentMonitor.on_new_block_event, 'ETHEREUM_MAINNET')
pub.subscribe(EthPaymentMonitor.on_new_block_event, 'ETHEREUM_MAINNET')

pub.subscribe(DucPaymentMonitor.on_new_block_event, 'DUCATUS_MAINNET')
pub.subscribe(DucxPaymentMonitor.on_new_block_event, 'DUCATUSX_MAINNET')

pub.subscribe(transfer.DucTransferMonitor.on_new_block_event, 'DUCATUS_MAINNET')
pub.subscribe(transfer.DucxTransferMonitor.on_new_block_event, 'DUCATUSX_MAINNET')
