from django.contrib import admin
from remusgold.store.models import Item, Group

# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class GroupAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Item, ItemAdmin)
admin.site.register(Group, GroupAdmin)