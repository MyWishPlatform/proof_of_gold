from django.db import models
from remusgold.store.models import Item
from remusgold.account.models import AdvUser
from remusgold.consts import MAX_AMOUNT_LEN
from remusgold.rates.api import get_usd_prices
from django.utils.timezone import now
from datetime import timedelta

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey('account.AdvUser', on_delete=models.CASCADE)
    required_usd_amount = models.DecimalField(max_digits=MAX_AMOUNT_LEN, decimal_places=2, null=True, blank=True)
    received_usd_amount = models.DecimalField(max_digits=MAX_AMOUNT_LEN, decimal_places=2, default=0)
    fixed_btc_rate = models.DecimalField(max_digits=MAX_AMOUNT_LEN, decimal_places=8)
    fixed_eth_rate = models.DecimalField(max_digits=MAX_AMOUNT_LEN, decimal_places=8)
    fixed_usdc_rate = models.DecimalField(max_digits=MAX_AMOUNT_LEN, decimal_places=8)
    status = models.CharField(max_length=50, default='WAITING_FOR_PAYMENT')
    created_date = models.DateTimeField(auto_now_add=True)
    time_to_live = models.IntegerField(default=3*60*60)

    def get_required_amount(self):
        payments = Payment.objects.filter(order=self)
        amount = 0
        for payment in payments:
            amount += payment.item.price * payment.quantity
        self.required_usd_amount = amount
        self.save()

    def is_active(self):
        """
        Return True if:
          * status is 'waiting'
          * time_to_live is more than time passed from model creation
        """
        if self.status not in ('UNDERPAYMENT', 'WAITING_FOR_PAYMENT'):
            return False
        return now() - self.created_at < timedelta(seconds=self.time_to_live)

    def fix_rates(self):
        usd_prices = get_usd_prices()
        self.fixed_btc_rate = usd_prices['BTC']
        self.fixed_eth_rate = usd_prices['ETH']
        self.fixed_usdc_rate = usd_prices['USDC']
        self.save()


class Payment(models.Model):
    order = models.ForeignKey('payments.Order', on_delete=models.CASCADE)
    item=models.ForeignKey('store.Item', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    currency = models.CharField(max_length=10)