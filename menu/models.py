from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

MAX_CHILDREN_ITEMS = 100

#TODO help_text

class MenuItem(models.Model):
    title = models.CharField(max_length=50)
    parent = models.ForeignKey('MenuItem', on_delete=models.CASCADE, null=True, blank=True)
    tooltip = models.CharField(max_length=200, null=True, blank=True)
    order = models.IntegerField(help_text="Order relative to its parent")

    def __str__(self):
        return self.title
    
    @classmethod
    def post_save(cls, sender, **kw):
        import ipdb; ipdb.set_trace()

class OrderedItem(MenuItem):
    '''
    Global ordering for items
    '''
    order = models.IntegerField()


receiver(post_save, sender=MenuItem)(MenuItem.post_save)