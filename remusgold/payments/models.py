from django.db import models
from django.utils.timezone import now
from datetime import timedelta

from remusgold.store.models import Item
from remusgold.account.models import AdvUser, ShippingAddress
from remusgold.consts import MAX_AMOUNT_LEN
from remusgold.rates.api import get_usd_prices


class Order(models.Model):
    '''
    Main model for orders, their rates calculations and so on
    '''
    user = models.ForeignKey('account.AdvUser', on_delete=models.CASCADE)
    required_usd_amount = models.DecimalField(max_digits=MAX_AMOUNT_LEN, decimal_places=2, null=True, blank=True)
    received_usd_amount = models.DecimalField(max_digits=MAX_AMOUNT_LEN, decimal_places=2, default=0)
    fixed_btc_rate = models.DecimalField(max_digits=MAX_AMOUNT_LEN, decimal_places=8, null=True)
    fixed_eth_rate = models.DecimalField(max_digits=MAX_AMOUNT_LEN, decimal_places=8, null=True)
    fixed_usdc_rate = models.DecimalField(max_digits=MAX_AMOUNT_LEN, decimal_places=8, null=True)
    status = models.CharField(max_length=50, default='WAITING_FOR_PAYMENT')
    created_date = models.DateTimeField(auto_now_add=True)
    time_to_live = models.IntegerField(default=3*60*60)
    currency = models.CharField(max_length=10, default='')
    shipping_address = models.OneToOneField('account.ShippingAddress', on_delete=models.SET_NULL, blank=True, null=True)


    def get_required_amount(self):
        '''
        get sum amount for order.
        '''
        payments = Payment.objects.filter(order=self)
        amount = 0
        for payment in payments:
            amount += payment.item.price * payment.quantity
        self.required_usd_amount = amount
        self.save()

    def is_active(self):
        """
        Return True if:
          * status is 'WAITING_FOR_PAYMENT'
          * time_to_live is more than time passed from model creation
        """
        if self.status not in ('WAITING_FOR_PAYMENT',):
            return False
        return now() - self.created_date < timedelta(seconds=self.time_to_live)

    def fix_rates(self):
        '''
        fix rates at order creation to negate rate fluctuations
        '''
        usd_prices = get_usd_prices()
        print(usd_prices)
        self.fixed_btc_rate = usd_prices['BTC']
        self.fixed_eth_rate = usd_prices['ETH']
        self.fixed_usdc_rate = usd_prices['USDT']
        self.save()


class Payment(models.Model):
    '''
    secondary model for items in Order models
    '''
    order = models.ForeignKey('payments.Order', on_delete=models.CASCADE)
    item = models.ForeignKey('store.Item', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
