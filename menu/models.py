import itertools
from math import ceil, log10

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver



#TODO help_text

class MenuItem(models.Model):
    MAX_CHILDREN_ITEMS = 100
    _order_digits = ceil(log10(MAX_CHILDREN_ITEMS))

    title = models.CharField(max_length=50)
    parent = models.ForeignKey('MenuItem', on_delete=models.CASCADE, null=True, blank=True)
    tooltip = models.CharField(max_length=200, null=True, blank=True)
    order = models.DecimalField(
        max_digits=_order_digits, decimal_places=0,
        help_text="Order relative to its parent",
    )

    

    def __str__(self):
        return self.title
    
    def get_global_order(self):
        obj = self.parent
        for i in itertools.count():
            if obj is None:
                break
            obj = obj.parent
        offset = self.MAX_CHILDREN_ITEMS ** i + self.order
        return offset + self.order

    @classmethod
    def post_save(cls, sender, instance=None, **kw):
        mo = MenuOrder(menu_item=instance, global_order=instance.get_global_order())
        mo.save()


class MenuOrder(models.Model):
    '''
    Global ordering for items
    '''
    MAX_NESTING = 20
    
    global_order = models.DecimalField(
        max_digits=MenuItem._order_digits * MAX_NESTING,
        decimal_places=0,
    )
    menu_item = models.OneToOneField('MenuItem', on_delete=models.CASCADE)


receiver(post_save, sender=MenuItem)(MenuItem.post_save)