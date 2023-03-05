import os

from models.product import Product


def setup_products_repository(folder, filename='products.csv', delimiter=';'):
    os.makedirs(folder, exist_ok=True)

    path = os.path.join(folder, filename)

    if not os.path.isfile(path):
        with open(path, 'w', encoding='utf-8') as file:
            header = Product.create_header(delimiter)
            file.write(f'{header}\n')

    return path


def load_all_products(path, delimiter=';'):
    products = []

    with open(path, encoding='utf-8') as file:
        file.readline()

        for line in file:
            product = Product.create_from_line(line, delimiter)
            products.append(product)

        return products


def save_all_products(path, products, delimiter=';'):
    with open(path, 'w', encoding='utf-8') as file:
        header = Product.create_header(delimiter)
        file.write(f'{header}\n')

        for product in products:
            line = product.to_line(delimiter)
            file.write(f'{line}\n')


def load_product(path, product_id, delimiter=';'):
    products = load_all_products(path, delimiter)

    for product in products:
        if product.product_id == product_id:
            return product

    return None


def create_product(path, product, delimiter=';'):
    products = load_all_products(path, delimiter)
    max_id = 0

    for stored_product in products:
        if stored_product.product_id > max_id:
            max_id = stored_product.product_id

    product.product_id = max_id + 1

    with open(path, 'a', encoding='utf-8') as file:
        line = product.to_line(delimiter)
        file.write(f'{line}\n')

    return product


def update_product(path, product, delimiter=';'):
    products = load_all_products(path, delimiter)
    updated_product = None

    for stored_product in products:
        if stored_product.product_id == product.product_id:
            stored_product.name = product.name
            stored_product.unit_price = product.unit_price
            stored_product.discount = product.discount
            updated_product = stored_product
            break

    if updated_product is not None:
        save_all_products(path, products, delimiter)

    return updated_product


def save_product(path, product, delimiter=';'):
    if product.product_id is None:
        # CREATE
        return create_product(path, product, delimiter)
    else:
        # UPDATE
        return update_product(path, product, delimiter)


def delete_product(path, product_id, delimiter=';'):
    products = load_all_products(path, delimiter)
    filtered = []
    deleted_product = None

    for product in products:
        if product.product_id != product_id:
            filtered.append(product)
        else:
            deleted_product = product

    if deleted_product is not None:
        save_all_products(path, filtered)

    return deleted_product
