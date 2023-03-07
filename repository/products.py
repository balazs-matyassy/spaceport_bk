from models.product import Product
from repository.repository import Repository


class ProductRepository(Repository):
    def __init__(self, folder, filename='products.csv', delimiter=';'):
        super().__init__(Product, folder, filename, delimiter)
