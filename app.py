from flask import Flask, render_template, request, redirect, url_for, flash

from models.product import Product
from repository.products import ProductRepository

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

product_repository = ProductRepository(app.instance_path)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/products')
def products_list():
    products = product_repository.load_all()
    return render_template('products/list.html', products=products)


@app.route('/products/create', methods=("GET", "POST"))
def products_create():
    product = Product(None, '', 0, 0)

    if request.method == "POST":
        product.name = request.form['name']
        product.unit_price = int(request.form['unit_price'])
        product.discount = int(request.form['discount'])
        product_repository.save(product)
        flash('Product created.')

        return redirect(url_for("products_list"))

    return render_template(
        'products/edit.html',
        create=True,
        product=product
    )


@app.route('/products/<int:product_id>/edit', methods=("GET", "POST"))
def products_edit(product_id):
    product = product_repository.load_by_id(product_id)

    if request.method == "POST":
        product.name = request.form['name']
        product.unit_price = int(request.form['unit_price'])
        product.discount = int(request.form['discount'])
        product_repository.save(product)
        flash('Product saved.')

    return render_template(
        'products/edit.html',
        create=False,
        product=product
    )


@app.route('/products/<int:product_id>/delete', methods=["POST"])
def products_delete(product_id):
    product_repository.delete(product_id)
    flash('Product deleted.')

    return redirect(url_for("products_list"))


if __name__ == '__main__':
    app.run()
