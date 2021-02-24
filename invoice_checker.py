import os
import sys
import time
import json
import requests
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'remusgold.settings')
import django

django.setup()

from remusgold.payments.models import Order

if __name__ == '__main__':
    while True:
        orders = Order.objects.filter(status="WAITING_FOR_PAYMENT")
        for order in orders:
            if not order.is_active():
                order.status = "EXPIRED"
                order.save()