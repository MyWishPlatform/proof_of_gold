from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from .utilities import get_timestamp_path
from remusgold.rates.models import UsdRate

# Create your models here.
class Group(models.Model):
    '''
    model for 2 categories in store - gold_bars and gold_coins
    '''
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    '''
    Base model for item in store.
    '''
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    images = models.ImageField(blank=True, upload_to=get_timestamp_path)
    total_supply = models.IntegerField()
    ducatus_bonus = models.FloatField()
    lucky_prize = models.FloatField()
    supply = models.IntegerField()
    reserved = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)
    price = models.FloatField()
    weight = models.IntegerField()
    description = models.CharField(max_length=1000, null=True, blank=True)
    winner = models.CharField(max_length=254, default=None, null=True, blank=True)

    def __str__(self):
        return self.name

    def update_price(self):
        try:
            gold_price = UsdRate.objects.get(currency='XAU').rate
        except ObjectDoesNotExist:
            return 'Can not get gold rate from db'
        self.price = round(self.weight * float(gold_price) * 1.03 * (1 + self.ducatus_bonus/100), 2)
        self.save()
        return 'price updated'

class Review(models.Model):
    '''
    model for item's reviews.
    field active=True allows publishing review.
    '''
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    rate = models.IntegerField()
    body = models.CharField(max_length=500)
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=False)
    email = models.EmailField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'reviews'
