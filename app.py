import functools

from flask import Flask, render_template, request, redirect, url_for, flash, session, g

from models.product import Product
from models.user import User
from repository.products import ProductRepository
from repository.users import UserRepository

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

user_repository = UserRepository(app.instance_path)
product_repository = ProductRepository(app.instance_path)


def fully_authenticated(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view


def admin_granted(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or not g.user.admin:
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view


@app.before_request
def load_current_user():
    if session.get('user_id') is None:
        g.user = None
    else:
        g.user = user_repository.load_by_id(session['user_id'])


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/products')
def products_list():
    products = product_repository.load_all()
    return render_template('products/list.html', products=products)


@app.route('/products/create', methods=("GET", "POST"))
@fully_authenticated
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
@fully_authenticated
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
@fully_authenticated
def products_delete(product_id):
    product_repository.delete(product_id)
    flash('Product deleted.')

    return redirect(url_for("products_list"))


@app.route('/users')
@admin_granted
def users_list():
    users = user_repository.load_all()
    return render_template('users/list.html', users=users)


@app.route('/users/create', methods=("GET", "POST"))
@admin_granted
def users_create():
    user = User(None, '', '')

    if request.method == "POST":
        user.username = request.form['username']
        user.password = request.form['password']
        user.admin = request.form['role'] == 'ADMIN'
        user_repository.save(user)
        flash('User created.')

        return redirect(url_for("users_list"))

    return render_template(
        'users/edit.html',
        create=True,
        user=user
    )


@app.route('/users/<int:user_id>/edit', methods=("GET", "POST"))
@admin_granted
def users_edit(user_id):
    user = user_repository.load_by_id(user_id)

    if request.method == "POST":
        user.username = request.form['username']
        user.password = request.form['password']
        user.admin = request.form['role'] == 'ADMIN'
        user_repository.save(user)
        flash('User saved.')

    return render_template(
        'users/edit.html',
        create=False,
        user=user
    )


@app.route('/users/<int:user_id>/delete', methods=["POST"])
@admin_granted
def users_delete(user_id):
    user_repository.delete(user_id)
    flash('User deleted.')

    return redirect(url_for("users_list"))


@app.route('/login', methods=("GET", "POST"))
def login():
    user = User(None, '', '')

    if request.method == "POST":
        user.username = request.form['username']
        user.password = request.form['password']

        stored_user = user_repository.load_by_username(user.username)

        if stored_user is not None and stored_user.password == user.password:
            session.clear()
            session['user_id'] = stored_user.user_id
            flash('Login successful.')

            return redirect(url_for('home'))
        else:
            flash('Wrong username or password.')

    return render_template('users/login.html', user=user)


@app.route('/logout')
def logout():
    session.clear()
    flash('Logout successful.')

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
