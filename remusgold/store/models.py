from django.db import models
from .utilities import get_timestamp_path

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
    ducatus_bonus = models.IntegerField()
    lucky_prize = models.FloatField()
    supply = models.IntegerField()
    sold = models.IntegerField()
    price = models.FloatField()
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

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
