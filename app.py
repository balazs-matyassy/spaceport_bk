import os

from flask import Flask, render_template

from repository.products import load_all_products, setup_products

PRODUCTS_PATH = None


def setup():
    global PRODUCTS_PATH

    os.makedirs(app.instance_path, exist_ok=True)
    PRODUCTS_PATH = os.path.join(app.instance_path, 'products.csv')
    setup_products(PRODUCTS_PATH)


app = Flask(__name__)
setup()


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/products')
def products_list():
    products = load_all_products(PRODUCTS_PATH)
    return render_template('products/list.html', products=products)


if __name__ == '__main__':
    app.run()
