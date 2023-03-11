from models.entity import Model


class Product(Model):
    def __init__(self, product_id, category_id, name, unit_price, discount=0):
        self.product_id = product_id
        self.category_id = category_id
        self.name = name
        self.unit_price = unit_price
        self.discount = discount

    @property
    def discounted_price(self):
        return round((self.unit_price * (100 - self.discount)) / 100)

    def get_id(self):
        return self.product_id

    def set_id(self, entity_id):
        self.product_id = entity_id
