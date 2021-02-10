from remusgold.payments.models import Order, Payment
from remusgold.account.models import AdvUser
from remusgold.store.models import Item
from remusgold.vouchers.models import Voucher
from remusgold.consts import DECIMALS

class TransferException(Exception):
    pass

def parse_payment_message(message):
    #FINDING ORDER
    order = Order.objects.filter(user_id=message['userID']).filter(status__in=('WAITING_FOR_PAYMENT', 'UNDERPAYMENT'))
    if not order:
        return 'Order not found'
    payment_usd_amount = message['amount'] / DECIMALS(message['currency']) #RATES
    #RATES!!!!
    order.received_usd_amount += payment_usd_amount
    if order.received_usd_amount < 0.995 * order.required_usd_amount:
        #UNDERPAYMENT LOGIC
        return 'underpayment'
    else:
        order.status = "PAID"
        order.save()
        payments = Payment.objects.filter(order=order)
        usd_amount = 0
        for payment in payments:
            item = Item.objects.get(id=payment.item_id)
            item.sold += payment.quantity
            item.supply -= payment.quantity
            item.save()

            usd_amount += item.price * payment.quantity * item.ducatus_bonus/100

        voucher = Voucher(
            payment=payments[0],
            user=AdvUser.objects.get(id=message['userID']),
            usd_amount=usd_amount)
        voucher.save()

        #SEND MAIL
        return 'correct payment'


    if order.received_usd_amount > 1.05 * order.required_usd_amount:
        #OVERPAYMENT LOGIC
        return 'overpayment'