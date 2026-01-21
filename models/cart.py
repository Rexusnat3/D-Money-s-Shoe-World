from datetime import datetime

class CartItem:
    def __init__(self, product_id, quantity):
        self._product_id = product_id
        self._quantity = quantity
        self._price = float(price)
        self._added_at = datetime.now()


class Cart:
    def __init__(self):
        self._items = []

    def add_item(self, item):
        self._items.append(item)

    def remove_item(self, item):
        self._items.remove(item)

    def get_items(self):
        return self._items