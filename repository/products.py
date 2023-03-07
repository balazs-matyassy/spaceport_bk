import os


def product_header(delimiter=';'):
    return 'id' \
        + delimiter + 'name' \
        + delimiter + 'unit_price'


def setup_products_repository(folder, filename='products.csv', delimiter=';'):
    os.makedirs(folder, exist_ok=True)

    path = os.path.join(folder, filename)

    if not os.path.isfile(path):
        with open(path, 'w', encoding='utf-8') as file:
            header = product_header(delimiter)
            file.write(f'{header}\n')

    return path


def line_to_product(line, delimiter=';'):
    line = line.strip()
    values = line.split(delimiter)

    if len(values) >= 3:
        return {
            'id': int(values[0].strip()),
            'name': values[1].strip(),
            'unit_price': int(values[2].strip())
        }
    else:
        return {
            'id': None,
            'name': values[0].strip(),
            'unit_price': int(values[1].strip())
        }


def product_to_line(product, delimiter=';'):
    return str(product['id']) \
        + delimiter + product['name'] \
        + delimiter + str(product['unit_price'])


def load_all_products(path, delimiter=';'):
    products = []

    with open(path, encoding='utf-8') as file:
        file.readline()

        for line in file:
            product = line_to_product(line, delimiter)
            products.append(product)

        return products


def save_all_products(path, products, delimiter=';'):
    with open(path, 'w', encoding='utf-8') as file:
        header = product_header(delimiter)
        file.write(f'{header}\n')

        for product in products:
            line = product_to_line(product, delimiter)
            file.write(f'{line}\n')


def load_product(path, product_id, delimiter=';'):
    products = load_all_products(path, delimiter)

    for product in products:
        if product['id'] == product_id:
            return product

    return None


def create_product(path, product, delimiter=';'):
    products = load_all_products(path, delimiter)
    max_id = 0

    for stored_product in products:
        if stored_product['id'] > max_id:
            max_id = stored_product['id']

    product['id'] = max_id + 1

    with open(path, 'a', encoding='utf-8') as file:
        line = product_to_line(product, delimiter)
        file.write(f'{line}\n')

    return product


def update_product(path, product, delimiter=';'):
    products = load_all_products(path, delimiter)
    updated_product = None

    for i in range(len(products)):
        if products[i]['id'] == product['id']:
            products[i] = product
            updated_product = products[i]
            break

    if updated_product is not None:
        save_all_products(path, products, delimiter)

    return updated_product


def save_product(path, product, delimiter=';'):
    if 'id' not in product or product['id'] is None:
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
        if product['id'] != product_id:
            filtered.append(product)
        else:
            deleted_product = product

    if deleted_product is not None:
        save_all_products(path, filtered)

    return deleted_product
