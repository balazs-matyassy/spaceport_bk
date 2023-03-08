from flask import Flask, render_template, request, redirect, url_for, flash

from models.product import Product
from models.user import User
from repository.products import ProductRepository
from repository.users import UserRepository

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

user_repository = UserRepository(app.instance_path)
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

        if product.name != '':
            product_repository.save(product)
            flash('Product created.')

            return redirect(url_for("products_list"))
        else:
            flash('Name missing.')

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


@app.route('/products/<int:product_id>/delete', methods=["POST"])
def products_delete(product_id):
    product_repository.delete(product_id)
    flash('Product deleted.')

    return redirect(url_for("products_list"))


@app.route('/users')
def users_list():
    users = user_repository.load_all()
    return render_template('users/list.html', users=users)


@app.route('/users/create', methods=("GET", "POST"))
def users_create():
    user = User(None, '', '')

    if request.method == "POST":
        user.username = request.form['username']
        user.password = request.form['password']
        user.admin = request.form['role'] == 'ADMIN'

        if user.username != '' and user.password != '':
            user_repository.save(user)
            flash('User created.')

            return redirect(url_for("users_list"))
        elif user.username == '':
            flash('Username missing.')
        else:
            flash('Password missing.')

    return render_template(
        'users/edit.html',
        create=True,
        user=user
    )


@app.route('/users/<int:user_id>/edit', methods=("GET", "POST"))
def users_edit(user_id):
    user = user_repository.load_by_id(user_id)

    if request.method == "POST":
        user.username = request.form['username']
        user.password = request.form['password']
        user.admin = request.form['role'] == 'ADMIN'

        if user.username != '' and user.password != '':
            user_repository.save(user)
            flash('User saved.')
        elif user.username == '':
            flash('Username missing.')
        else:
            flash('Password missing.')

    return render_template(
        'users/edit.html',
        create=False,
        user=user
    )


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_delete(user_id):
    user_repository.delete(user_id)
    flash('User deleted.')

    return redirect(url_for("users_list"))


if __name__ == '__main__':
    app.run()
