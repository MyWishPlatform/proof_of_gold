from pubsub import pub

from eventscanner.monitors.payments import (BTCPaymentMonitor,
                                            EthPaymentMonitor,
                                            ERC20PaymentMonitor)

pub.subscribe(BTCPaymentMonitor.on_new_block_event, 'BTC_MAINNET')
pub.subscribe(ERC20PaymentMonitor.on_new_block_event, 'ETHEREUM_MAINNET')
pub.subscribe(EthPaymentMonitor.on_new_block_event, 'ETHEREUM_MAINNET')