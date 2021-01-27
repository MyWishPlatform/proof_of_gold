from django.db import models
from remusgold.store.models import Item
from remusgold.account.models import AdvUser

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey('account.AdvUser', on_delete=models.CASCADE)
    item=models.ForeignKey('store.Item', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)