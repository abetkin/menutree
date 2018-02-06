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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('menuorder__global_order')


@admin.register(MenuOrder)
class MenuOrderAdmin(admin.ModelAdmin):
    pass