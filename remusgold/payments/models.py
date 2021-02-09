from django.db import models
from remusgold.store.models import Item
from remusgold.account.models import AdvUser
from remusgold.consts import MAX_AMOUNT_LEN

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey('account.AdvUser', on_delete=models.CASCADE)
    required_usd_amount = models.DecimalField(max_digits=MAX_AMOUNT_LEN, decimal_places=0, null=True, blank=True)
    received_usd_amount = models.DecimalField(max_digits=MAX_AMOUNT_LEN, decimal_places=0)
    status = models.CharField(max_length=50, default='WAITING_FOR_PAYMENT')
    created_date = models.DateTimeField(auto_now_add=True)

    def get_required_amount(self):
        payments = Payment.objects.filter(order=self)
        amount = 0
        for payment in payments:
            amount += payment.item.price * payment.quantity
        self.required_usd_amount = amount
        self.save()


class Payment(models.Model):
    order = models.ForeignKey('payments.Order', on_delete=models.CASCADE)
    item=models.ForeignKey('store.Item', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    currency = models.CharField(max_length=10)