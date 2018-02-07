from django.contrib import admin
from django import forms
from django.forms import formsets

# Register your models here.

from .models import *

class MenuItems(admin.TabularInline):
    model = MenuItem

    def get_formset(self, request, obj=None, **kwargs):
        kwargs.update(
            fields=[
                'title', 'tooltip', 'order',
            ]
        )
        fs = super().get_formset(request, **kwargs)
        class MenuItemsFormSet(fs):
            
            def save(self, commit=False):
                objects = super().save(commit=False)
                existing = [
                    o.pk for o in objects if o.pk is not None
                ]
                self.model.objects.filter(pk__in=existing).delete()
                orders_list = [o.order for o in objects]
                if not all(o is not None for o in orders_list):
                    orders_list = range(1, len(objects) + 1)
                for obj, order in zip(objects, orders_list):
                    obj.pk = None
                    obj.order = order
                    obj.save()
                return objects

        return MenuItemsFormSet


def global_id(obj):
    return str(obj.globalid.global_id).lstrip('0.').strip('0')
global_id.short_description = 'Global Id'

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    inlines = [
        MenuItems
    ]
    fields = [
        'title', 'parent', 'tooltip', 'order'
    ]

    list_display = [global_id, 'title']
    ordering = ['globalid__global_id']
