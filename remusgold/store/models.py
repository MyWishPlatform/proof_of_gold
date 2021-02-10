from django.db import models
from .utilities import get_timestamp_path

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Item(models.Model):
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
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    rate = models.IntegerField()
    body = models.CharField(max_length=500)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'reviews'
