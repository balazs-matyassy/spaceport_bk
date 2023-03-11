from models.product import Product
from repository.repository import Repository


class ProductRepository(Repository):
    def __init__(self, folder, filename='products.csv', delimiter=';'):
        super().__init__(folder, filename, delimiter)

    def load_all_by_category(self, category_id):
        products = self.find_all()
        filtered = []

        for product in products:
            if product.category_id == category_id:
                filtered.append(product)

        return filtered

    def delete_by_category(self, category_id):
        products = self.find_all()
        filtered = []

        for product in products:
            if product.category_id != category_id:
                filtered.append(product)

        deleted = len(products) > len(filtered)

        if deleted > 0:
            self.overwrite(filtered)

        return deleted

    def _get_header(self):
        return 'id' \
            + self.delimiter + 'category_id' \
            + self.delimiter + 'name' \
            + self.delimiter + 'unit_price' \
            + self.delimiter + 'discount'

    def _line_to_entity(self, line):
        line = line.strip()
        values = line.split(self.delimiter)

        if len(values) >= 5:
            return Product(
                int(values[0].strip()), int(values[1].strip()),
                values[2].strip(), int(values[3].strip()), int(values[4].strip())
            )
        elif len(values) >= 4:
            return Product(None, int(values[0].strip()), values[1].strip(), int(values[2]), int(values[3]))
        else:
            return Product(None, int(values[0].strip()), values[1].strip(), int(values[2]))

    def _entity_to_line(self, product):
        return str(product.product_id) \
            + self.delimiter + str(product.category_id) \
            + self.delimiter + product.name \
            + self.delimiter + str(product.unit_price) \
            + self.delimiter + str(product.discount)
