import itertools
from math import ceil, log10

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .threadlocal import get_menu_item_order

#TODO help_text

class MenuItem(models.Model):
    MAX_NESTING = 20
    MAX_CHILDREN_ITEMS = 100
    _order_digits = ceil(log10(MAX_CHILDREN_ITEMS))

    title = models.CharField(max_length=50)
    parent = models.ForeignKey('MenuItem', on_delete=models.CASCADE, null=True, blank=True)
    tooltip = models.CharField(max_length=200, null=True, blank=True)
    order = models.DecimalField(
        max_digits=_order_digits, decimal_places=0,
        null=True, blank=True,
        help_text="Order relative to its parent",
    )
    global_order = models.DecimalField(
        max_digits=_order_digits * MAX_NESTING,
        decimal_places=0,
        null=True, blank=True,
    )

    def __str__(self):
        return self.title

    def save(self, **kw):
        if self.order is None:
            self.set_order()
        super().save(**kw)

    def set_order(self):
        self.order = get_menu_item_order(self)
        self.global_order = self._get_global_order(self.order) \
            if self.order is not None else None

    def _get_global_order(self, order):
        obj = self.parent
        for i in itertools.count():
            if obj is None:
                break
            obj = obj.parent
        return self.MAX_CHILDREN_ITEMS ** i + order

