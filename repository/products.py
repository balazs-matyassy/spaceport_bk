from models.product import Product
from repository.repository import Repository


class ProductRepository(Repository):
    def __init__(self, folder, filename='products.csv', delimiter=';'):
        super().__init__(Product, folder, filename, delimiter)

    def load_all_by_category(self, category_id):
        products = self.load_all()
        filtered = []

        for product in products:
            if product.category_id == category_id:
                filtered.append(product)

        return filtered

    def delete_by_category(self, category_id):
        products = self.load_all()
        filtered = []

        for product in products:
            if product.category_id != category_id:
                filtered.append(product)

        deleted = len(products) > len(filtered)

        if deleted > 0:
            self.save_all(filtered)

        return deleted
