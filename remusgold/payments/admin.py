from django.contrib import admin

from remusgold.payments.models import Payment, Order


class PaymentAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class PaymentInline(admin.TabularInline):
    model = Payment
    readonly_fields = ('id',)

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    inlines = (PaymentInline,)


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)