from django.contrib import admin
from remusgold.rates.models import UsdRate


class UsdRateAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(UsdRate, UsdRateAdmin)