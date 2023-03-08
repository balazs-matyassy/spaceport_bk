from flask import Flask, render_template, request, redirect, url_for

from repository.products import load_all_products, setup_products_repository, save_product, load_product, delete_product

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

PRODUCTS_PATH = setup_products_repository(app.instance_path)


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

        if product['name'] != '':
            save_product(PRODUCTS_PATH, product)

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

        if product['name'] != '':
            save_product(PRODUCTS_PATH, product)

    return render_template(
        'products/edit.html',
        create=False,
        product=product
    )


@app.route('/products/<int:product_id>/delete', methods=["POST"])
def products_delete(product_id):
    delete_product(PRODUCTS_PATH, product_id)
    return redirect(url_for("products_list"))


if __name__ == '__main__':
    app.run()
