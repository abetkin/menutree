from django.contrib import admin
from django import forms
from django.forms import formsets
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

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

            def save(self, commit=True):
                """
                Set the default values for the order of menu items,
                in case it's not provided
                """
                extra_forms = [
                    f for f in self.extra_forms if f.has_changed()
                ]
                objects = [
                    f.instance for f in self.initial_forms + extra_forms
                ]
                if all(
                    o.order is None
                    for o in objects
                ):
                    for i, o in enumerate(objects):
                        o.order = i + 1
                super().save(commit=commit)

            def full_clean(self):
                """
                Check that order of menu items is valid, in case it is provided
                for every menu item
                """
                super().full_clean()
                if not hasattr(self, 'cleaned_data'):
                    return
                data = [
                    d for d in self.cleaned_data if d
                ]
                orders = {o['order'] for o in data}
                if orders == {None}:
                    # Order is not provided, nothing to validate
                    return
                if orders != set(range(1, len(data) + 1)):
                    e = ValidationError(
                        message=f"Menu items should have orders from 1 to {len(data)}"
                    )
                    self._non_form_errors = self.error_class(e.error_list)

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
