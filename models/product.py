from models.model import Model


class Product(Model):
    def __init__(self, product_id, category_id, name, unit_price, discount=0):
        self.product_id = product_id
        self.category_id = category_id
        self.name = name
        self.unit_price = unit_price
        self.discount = discount

    @staticmethod
    def create_header(delimiter=';'):
        return 'id' \
            + delimiter + 'category_id' \
            + delimiter + 'name' \
            + delimiter + 'unit_price' \
            + delimiter + 'discount'

    @staticmethod
    def create_from_line(line, delimiter=';'):
        line = line.strip()
        values = line.split(delimiter)

        if len(values) >= 5:
            return Product(
                int(values[0].strip()), int(values[1].strip()),
                values[2].strip(), int(values[3].strip()), int(values[4].strip())
            )
        elif len(values) >= 4:
            return Product(None, int(values[0].strip()), values[1].strip(), int(values[2]), int(values[3]))
        else:
            return Product(None, int(values[0].strip()), values[1].strip(), int(values[2]))

    @property
    def discounted_price(self):
        return round((self.unit_price * (100 - self.discount)) / 100)

    def get_id(self):
        return self.product_id

    def set_id(self, entity_id):
        self.product_id = entity_id

    def to_line(self, delimiter=';'):
        return str(self.product_id) \
            + delimiter + str(self.category_id) \
            + delimiter + self.name \
            + delimiter + str(self.unit_price) \
            + delimiter + str(self.discount)
