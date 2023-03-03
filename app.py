import os

from flask import Flask, render_template, request, redirect, url_for, flash

from repository.products import load_all_products, setup_products, save_product, load_product, delete_product

PRODUCTS_PATH = None


def setup():
    global PRODUCTS_PATH

    os.makedirs(app.instance_path, exist_ok=True)
    PRODUCTS_PATH = os.path.join(app.instance_path, 'products.csv')
    setup_products(PRODUCTS_PATH)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
setup()


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/products')
def products_list():
    products = load_all_products(PRODUCTS_PATH)
    return render_template('products/list.html', products=products)


@app.route('/products/create', methods=("GET", "POST"))
def products_create():
    product = {
        'name': '',
        'unit_price': 0
    }

    if request.method == "POST":
        product['name'] = request.form['name']
        product['unit_price'] = int(request.form['unit_price'])
        save_product(PRODUCTS_PATH, product)
        flash('Product created.')

        return redirect(url_for("products_list"))

    return render_template(
        'products/edit.html',
        create=True,
        product=product
    )


@app.route('/products/<int:product_id>/edit', methods=("GET", "POST"))
def products_edit(product_id):
    product = load_product(PRODUCTS_PATH, product_id)

    if request.method == "POST":
        product['name'] = request.form['name']
        product['unit_price'] = int(request.form['unit_price'])
        save_product(PRODUCTS_PATH, product)
        flash('Product saved.')

    return render_template(
        'products/edit.html',
        create=False,
        product=product
    )


@app.route('/products/<int:product_id>/delete', methods=["POST"])
def products_delete(product_id):
    delete_product(PRODUCTS_PATH, product_id)
    flash('Product deleted.')

    return redirect(url_for("products_list"))


if __name__ == '__main__':
    app.run()
