class Product:
    def __init__(self, product_id, name, unit_price, discount=0):
        self.product_id = product_id
        self.name = name
        self.unit_price = unit_price
        self.discount = discount

    @staticmethod
    def create_header(delimiter=';'):
        return 'id' \
            + delimiter + 'name' \
            + delimiter + 'unit_price' \
            + delimiter + 'discount'

    @staticmethod
    def create_from_line(line, delimiter=';'):
        line = line.strip()
        values = line.split(delimiter)

        if len(values) >= 4:
            return Product(int(values[0].strip()), values[1].strip(), int(values[2].strip()), int(values[3].strip()))
        elif len(values) >= 3:
            return Product(None, values[0].strip(), int(values[1].strip()), int(values[2].strip()))
        else:
            return Product(None, values[0].strip(), int(values[1].strip()))

    @property
    def discounted_price(self):
        return round((self.unit_price * (100 - self.discount)) / 100)

    def to_line(self, delimiter=';'):
        return str(self.product_id) \
            + delimiter + self.name \
            + delimiter + str(self.unit_price) \
            + delimiter + str(self.discount)
