from flask import Blueprint, render_template, request, flash, redirect, url_for

from auth import fully_authenticated
from db import get_product_repository
from models.product import Product

bp = Blueprint('products', __name__, url_prefix="/products")


@bp.route('/')
def products_list():
    product_repository = get_product_repository()
    products = product_repository.load_all()
    return render_template('products/list.html', products=products)


@bp.route('/create', methods=("GET", "POST"))
@fully_authenticated
def products_create():
    product = Product(None, '', 0, 0)

    if request.method == "POST":
        product.name = request.form['name']
        product.unit_price = int(request.form['unit_price'])
        product.discount = int(request.form['discount'])

        if product.name != '':
            product_repository = get_product_repository()
            product_repository.save(product)

            flash('Product created.')

            return redirect(url_for("products.products_list"))
        else:
            flash('Name missing.')

    return render_template(
        'products/edit.html',
        create=True,
        product=product
    )


@bp.route('/<int:product_id>/edit', methods=("GET", "POST"))
@fully_authenticated
def products_edit(product_id):
    product_repository = get_product_repository()
    product = product_repository.load_by_id(product_id)

    if request.method == "POST":
        product.name = request.form['name']
        product.unit_price = int(request.form['unit_price'])
        product.discount = int(request.form['discount'])

        if product.name != '':
            product_repository.save(product)
            flash('Product saved.')
        else:
            flash('Name missing.')

    return render_template(
        'products/edit.html',
        create=False,
        product=product
    )


@bp.route('/<int:product_id>/delete', methods=["POST"])
@fully_authenticated
def products_delete(product_id):
    product_repository = get_product_repository()
    product_repository.delete(product_id)
    flash('Product deleted.')

    return redirect(url_for("products.products_list"))
