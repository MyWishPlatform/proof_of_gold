import os
import sys
import time
import json
import requests
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'remusgold.settings')
import django

django.setup()

from remusgold.payments.models import Order, Payment
from remusgold.store.models import Item

if __name__ == '__main__':
    while True:
        '''
        checking if order is expired
        '''
        orders = Order.objects.filter(status="WAITING_FOR_PAYMENT")
        for order in orders:
            if not order.is_active():
                order.status = "EXPIRED"
                order.save()
                payments = Payment.objects.filter(order=order)
                for payment in payments:
                    item = Item.objects.get(id=payment.item_id)
                    item.supply += payment.quantity
                    item.reserved -= payment.quantity
                    item.save()
        print('sleeping')
        time.sleep(600)
