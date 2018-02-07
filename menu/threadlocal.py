
import threading

storage = threading.local()
storage.menu_order = {}


def get_menu_item_order(instance):
    data = storage.menu_order
    if not data.get('parent'):# or not instance.parent == data['parent']:
        data['parent'] = instance
        return 0
    if 'count' not in data:
        data['count'] = 1
    else:
        data['count'] += 1
    return data['count']

def fire_menu_save_started():
    # assert {}
    storage.menu_order = {}

def fire_menu_save_end():
    # opt
    # check and log
    storage.menu_order = {}