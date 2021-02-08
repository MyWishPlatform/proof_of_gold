from django.db import models
from remusgold.consts import MAX_AMOUNT_LEN


class Transfer(models.Model):
    voucher = models.ForeignKey('vouchers.Voucher', on_delete=models.CASCADE, null=True, default=None)
    amount = models.DecimalField(max_digits=MAX_AMOUNT_LEN, decimal_places=0)
    currency = models.CharField(max_length=10)
    duc_address = models.CharField(max_length=50)
    tx_hash = models.CharField(max_length=100)
    tx_error = models.TextField(default='')
    status = models.CharField(max_length=50, default='WAITING FOR TRANSFER')
    creation_datetime = models.DateTimeField(auto_now_add=True)