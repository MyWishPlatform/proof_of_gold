from django.contrib import admin
from remusgold.vouchers.models import Voucher

# Register your models here.
class VoucherAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Voucher, VoucherAdmin)