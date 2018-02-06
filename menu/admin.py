from django.contrib import admin

# Register your models here.

from menu.models import *

class MenuItems(admin.TabularInline):
    model = MenuItem

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    inlines = [
        MenuItems
    ]

    # def get_queryset(self, request):
    #     import ipdb; ipdb.set_trace()
    #     qs = super().get_queryset(request)
    #     return [qs.first()]