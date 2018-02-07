from django.contrib import admin

# Register your models here.

from .models import *
from .threadlocal import fire_menu_save_started

class MenuItems(admin.TabularInline):
    model = MenuItem

    def get_formset(self, request, obj=None, **kwargs):
        kwargs.update(
            fields=[
                'title', 'tooltip', 'id',
            ]
        )
        return super().get_formset(request, **kwargs)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    inlines = [
        MenuItems
    ]

    list_display = ['global_order', 'title']

    def _create_formsets(self, *args, **kw):
        #
        fire_menu_save_started()
        return super()._create_formsets(*args, **kw)

    ordering = ['global_order']

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.order_by('menuorder__global_order')

