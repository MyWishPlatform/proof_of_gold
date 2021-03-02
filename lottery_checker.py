import os
import sys
import time
import json
import requests
import traceback
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'remusgold.settings')
import django

django.setup()

from remusgold.store.models import Item
from remusgold.payments.models import Order, Payment

def finalize_lottery(item):
    '''
    get winner's coin with randint(), find winning order, get winner's email
    '''
    win_number = random.randint(1, item.total_supply)
    print(f'got winner number: {win_number}')
    active_payments = Payment.objects.filter(item=item).filter(order__status='PAID')

    #checking that amounts are equal
    sum_sold=0
    for payment in active_payments:
        sum_sold += payment.quantity
    if sum_sold != item.total_supply:
        print(f'SUSPICIOUS: item total supply {item.total_supply} is not equal to sold items {sum_sold}, cancelling lottery')
        return 'error'

    coins_counted = 0
    for payment in active_payments:
        coins_counted += payment.quantity
        if coins_counted >= win_number:
            winner_payment = payment
            print(f'found winner payment: {payment.id}')
            break
    if winner_payment:
        winner = winner_payment.order.user.email
        print(f'winner is {winner}')
        return winner
    else:
        print('SUSPICIOUS: did not get winning payment, cancelling lottery')
        return 'error'


if __name__ == '__main__':
    while True:
        print('Starting Polling')
        items = Item.objects.all()
        for item in items:
            if item.supply == 0 and not item.winner:
                print(f'\nStarting lottery for item {item.name}')
                winner = finalize_lottery(item)
                item.winner = winner
                item.save()
        print('sleeping')
        time.sleep(600)