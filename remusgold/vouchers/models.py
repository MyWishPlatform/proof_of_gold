import secrets
import requests
import json

from django.db import models
from django.utils import timezone
from remusgold.consts import DECIMALS
from remusgold.transfers.models import Transfer
from remusgold.transfers.api import duc_transfer
from remusgold.settings_local import RATES_API_URL

class Voucher(models.Model):
    '''
    Base voucher model.
    field activation_code should be added with "PG-" at the beginning for correct redirecting form wallet frontend.
    (currently hardcoded in voucher creation (function process_correct_payment() in payments/api.py))
    '''
    user = models.ForeignKey('account.AdvUser', on_delete=models.CASCADE)
    payment = models.OneToOneField('payments.Payment', on_delete=models.CASCADE, null=True)
    activation_code = models.CharField(max_length=50, unique=True, default=secrets.token_urlsafe)
    usd_amount = models.DecimalField(max_digits=100, decimal_places=2)
    is_used = models.BooleanField(default=False)
    is_email_sent = models.BooleanField(default=False)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    activation_datetime = models.DateTimeField(null=True, default=None)

    def activate(self, address):
        rate = json.loads(requests.get(RATES_API_URL.format(fsym='DUC', tsyms='USD')).content).get('USD')
        token_amount = int(int(self.usd_amount * (DECIMALS['DUC']))/rate)
        transfer = Transfer(
            voucher=self,
            amount=token_amount,
            currency='DUC',
            duc_address=address,
        )
        try:
            transfer.tx_hash = duc_transfer(address, token_amount)
            transfer.status = 'WAITING FOR CONFIRM'
            self.is_used = True
            self.activation_datetime = timezone.now()
            self.save()
        except Exception as e:
            transfer.tx_error = repr(e)
            transfer.status = 'FAIL'
        transfer.save()
        return transfer
