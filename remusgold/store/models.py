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
    supply = models.IntegerField()
    sold = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return self.name
