from django.contrib import admin
from remusgold.store.models import Item, Group, Review

# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class GroupAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Item, ItemAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Review, ReviewAdmin)