from django.contrib import admin

from remusgold.account.models import AdvUser, ShippingAddress, BillingAddress


class AdvUserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class ShippingAddressAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class BillingAddressAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(AdvUser, AdvUserAdmin)
admin.site.register(BillingAddress, BillingAddressAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)