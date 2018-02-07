import itertools
from math import ceil, log10

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class GlobalId(models.Model):
    MAX_NESTING = 20
    ORDER_DIGITS = 2

    global_id = models.DecimalField(
        max_digits=ORDER_DIGITS * MAX_NESTING + 2,
        decimal_places=ORDER_DIGITS * MAX_NESTING,
    )
    menu_item = models.OneToOneField('MenuItem', on_delete=models.CASCADE)

    @classmethod
    def get_global_id(cls, menu_item):
        orders_list = []
        obj = menu_item
        for i in itertools.count():
            orders_list.append(obj.order)
            obj = obj.parent
            if obj is None:
                break
        orders_list = [
            '{:02.0f}'.format(v) for v in reversed(orders_list)
        ]
        return ''.join(['0.'] + orders_list)


class MenuItem(models.Model):
    title = models.CharField(max_length=50)
    parent = models.ForeignKey('MenuItem', on_delete=models.CASCADE, null=True, blank=True)
    tooltip = models.CharField(max_length=200, null=True, blank=True)
    order = models.IntegerField(
        null=True, blank=True,
        help_text="Order relative to its parent",
    )

    def __str__(self):
        return self.title

    def save(self, **kw):
        if self.order is None:
            self.order = self.get_default_order()
        super().save(**kw)

    def get_default_order(self):
        return self.__class__.objects.filter(parent__isnull=True).count() + 1



@receiver(post_save, sender=MenuItem)
def post_save(sender, instance=None, **kwargs):
    global_id = GlobalId.get_global_id(instance)
    obj, created = GlobalId.objects.get_or_create(
        defaults={'global_id': global_id},
        menu_item=instance,
    )
    if not created:
        obj.global_id = global_id
    obj.save()