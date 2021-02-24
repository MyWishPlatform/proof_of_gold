from remusgold.payments.models import Order, Payment
from remusgold.account.models import AdvUser, ShippingAddress
from remusgold.store.models import Item
from remusgold.vouchers.models import Voucher
from remusgold.consts import DECIMALS
from remusgold.transfers.api import eth_return_transfer, btc_return_transfer, usdc_return_transfer
from remusgold.account.models import get_mail_connection
from remusgold.templates.email.payment_letter_body import order_body, order_style, item_body, ending_body
from django.core.mail import send_mail
from remusgold.settings import EMAIL_HOST_USER, EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_HOST_PASSWORD


class TransferException(Exception):
    pass

def parse_payment_message(message):
    #FINDING ORDER
    orders = Order.objects.filter(user_id=message['userID']).filter(status__in=('WAITING_FOR_PAYMENT', 'UNDERPAYMENT'))
    active_order= False
    if not orders:
        return 'Order not found'
    for order in orders:
        if order.is_active() and order.currency.lower() == message['currency'].lower():
            active_order = order
            break
    if not active_order:
        print('Active order not found, cancelling payment checker')
        return 'no order'
    currency = message['currency']
    payment_usd_amount = message['amount'] / float(DECIMALS[message['currency']]) * float(getattr(active_order, f'fixed_{currency.lower()}_rate'))
    active_order.received_usd_amount = float(active_order.received_usd_amount) + payment_usd_amount
    print(active_order.received_usd_amount, active_order.required_usd_amount)
    if float(active_order.received_usd_amount) < 0.995 * float(active_order.required_usd_amount):
        active_order.status = 'UNDERPAYMENT'
        active_order.save()
        #ANY MESSAGES TO USER?
        return 'underpayment'
    elif float(active_order.received_usd_amount) > 1.05 * float(active_order.required_usd_amount):
        process_correct_payment(active_order)
        process_overpayment(active_order, message)
        return 'overpayment'
    else:
        process_correct_payment(active_order)
        return 'correct payment'

def process_correct_payment(active_order):
    active_order.status = "PAID"
    active_order.save()
    payments = Payment.objects.filter(order=active_order)
    usd_amount = 0
    html_items = ''
    if active_order.currency == 'ETH':
        paid_by = 'ETH'
    elif active_order.currency == 'BTC':
        paid_by = 'BTC'
    elif active_order.currency == 'USDC':
        paid_by = 'USDC'
    else:
        paid_by = 'Credit Card'
    for payment in payments:
        item = Item.objects.get(id=payment.item_id)
        item.sold += payment.quantity
        item.supply -= payment.quantity
        item.save()

        usd_amount += item.price * payment.quantity * item.ducatus_bonus / 100
        html_break = item.name.split('–')
        print(html_break)

        html_item = item_body.format(
            item_name = html_break[1], weight = html_break[0], amount = item.price,
            bonus = item.ducatus_bonus, paid_by = paid_by,
        )
        html_items+=html_item

    voucher = Voucher(
        payment=payments[0],
        user=AdvUser.objects.get(id=active_order.user_id),
        usd_amount=usd_amount)
    voucher.save()
    user = AdvUser.objects.get(id=active_order.user_id)
    shipping = ShippingAddress.objects.get(id=user.shipping_address_id)
    connection = get_mail_connection()
    html_body = order_body.format(
        first_name = shipping.first_name, last_name = shipping.last_name, email = user.email,
        phone = shipping.phone, payments = payments,
        delivery_address = shipping.country + ', ' + shipping.county + ', ' + shipping.town + ', ' + shipping.full_address,
    )
    html_ending = ending_body.format(code = voucher.activation_code)



    send_mail(
        'Payment Confirmation',
        '',
        EMAIL_HOST_USER,
        [user.email],
        connection=connection,
        html_message = order_style + html_body + html_items + html_ending,
    )

def process_overpayment(active_order, message):
    currency = message['currency']
    delta = (float(active_order.received_usd_amount) - float(active_order.required_usd_amount)) /float(getattr(active_order, f'fixed_{currency.lower()}_rate')) * DECIMALS[currency]
    currency = active_order.currency
    if currency == 'ETH':
        return_transfer = eth_return_transfer(active_order, int(delta), message)
    if currency == 'USDC':
        pass
        return_transfer = usdc_return_transfer(active_order, int(delta), message)
    if currency == 'BTC':
        return_transfer = btc_return_transfer(active_order, int(delta), message)

