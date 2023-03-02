import os

from flask import Flask, render_template, request, redirect, url_for

from repository.products import load_all_products, setup_products, save_product

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
def list_products():
    products = load_all_products(PRODUCTS_PATH)
    return render_template('products/list.html', products=products)


@app.route('/products/create', methods=("GET", "POST"))
def create_product():
    product = {
        'name': '',
        'unit_price': 0
    }

    if request.method == "POST":
        product['name'] = request.form['name']
        product['unit_price'] = int(request.form['unit_price'])
        save_product(PRODUCTS_PATH, product)

        return redirect(url_for("list_products"))

    return render_template(
        'products/create.html', product=product)


if __name__ == '__main__':
    app.run()
