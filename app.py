from flask import Flask

from repository.products import load_all_products, setup_products_repository, save_product, load_product, delete_product


def input_cmd():
    line = input('>> ').strip()
    values = line.split(' ', 1)

    return {
        'name': values[0].strip(),
        'param': values[1] if len(values) >= 2 else None
    }


app = Flask(__name__)

PRODUCTS_PATH = setup_products_repository(app.instance_path)

print('==================================================')
print('\tWelcome to SpacePort 0.1')
print('==================================================')

cmd = input_cmd()

while cmd['name'] != 'exit':
    if cmd['name'] == 'list':
        products = load_all_products(PRODUCTS_PATH)

        print(f'{"ID":4} {"Name":32} {"Unit price":8}')

        for product in products:
            print(f'{product["id"]:4} {product["name"]:32} {product["unit_price"]:8}')
    elif cmd['name'] == 'view':
        product = load_product(PRODUCTS_PATH, int(cmd['param']))
        print(f'{"ID":4} {"Name":32} {"Unit price":8}')
        print(f'{product["id"]:4} {product["name"]:32} {product["unit_price"]:8}')
    elif cmd['name'] == 'save':
        product = line_to_product(cmd['param'], delimiter=',')
        save_product(PRODUCTS_PATH, product)
        print('Product saved.')
    elif cmd['name'] == 'delete':
        delete_product(PRODUCTS_PATH, int(cmd['param']))
        print('Product deleted.')
    elif cmd['name'] == 'help':
        print('Available commands:')
        print('- list')
        print('- view [id]')
        print('- save [name],[unit_price]')
        print('\t-> create new product')
        print('- save [id],[name],[unit_price]')
        print('\t-> update existing product')
        print('- delete [id]')
        print('- help')
        print('- exit')
    else:
        print('Wrong command!')

    cmd = input_cmd()

print('Bye! :)')
