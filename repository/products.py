import os

from models.product import Product


class ProductRepository:
    def __init__(self, folder, filename='products.csv', delimiter=';'):
        os.makedirs(folder, exist_ok=True)

        self.path = os.path.join(folder, filename)
        self.delimiter = delimiter

        if not os.path.isfile(self.path):
            with open(self.path, 'w', encoding='utf-8') as file:
                header = Product.create_header(self.delimiter)
                file.write(f'{header}\n')

    def load_all(self):
        products = []

        with open(self.path, encoding='utf-8') as file:
            file.readline()

            for line in file:
                product = Product.create_from_line(line, self.delimiter)
                products.append(product)

            return products

    def save_all(self, products):
        with open(self.path, 'w', encoding='utf-8') as file:
            header = Product.create_header(self.delimiter)
            file.write(f'{header}\n')

            for product in products:
                line = product.to_line(self.delimiter)
                file.write(f'{line}\n')

    def load_by_id(self, product_id):
        products = self.load_all()

        for product in products:
            if product.product_id == product_id:
                return product

        return None

    def save(self, product):
        if product.product_id is None:
            # CREATE
            return self.__create(product)
        else:
            # UPDATE
            return self.__update(product)

    def delete(self, product_id):
        products = self.load_all()
        filtered = []
        deleted_product = None

        for product in products:
            if product.product_id != product_id:
                filtered.append(product)
            else:
                deleted_product = product

        if deleted_product is not None:
            self.save_all(filtered)

        return deleted_product

    def __create(self, product):
        products = self.load_all()
        max_id = 0

        for stored_product in products:
            if stored_product.product_id > max_id:
                max_id = stored_product.product_id

        product.product_id = max_id + 1

        with open(self.path, 'a', encoding='utf-8') as file:
            line = product.to_line(self.delimiter)
            file.write(f'{line}\n')

        return product

    def __update(self, product):
        products = self.load_all()
        updated_product = None

        for i in range(len(products)):
            if products[i].product_id == product.product_id:
                products[i] = product
                updated_product = products[i]
                break

        if updated_product is not None:
            self.save_all(products)

        return updated_product
