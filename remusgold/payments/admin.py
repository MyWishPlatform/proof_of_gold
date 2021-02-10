from django.contrib import admin
from remusgold.payments.models import Payment, Order

# Register your models here.
class PaymentAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)