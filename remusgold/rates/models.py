from django.db import models

from remusgold.consts import MAX_AMOUNT_LEN


class UsdRate(models.Model):
    '''
    Absolutely typical rate app for winter 2021.
    '''
    currency = models.CharField(max_length=20)
    rate = models.DecimalField(max_digits=MAX_AMOUNT_LEN, decimal_places=8)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.currency