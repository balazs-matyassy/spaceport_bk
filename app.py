from flask import Flask, render_template

from repository.products import load_all_products, setup_products_repository

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


if __name__ == '__main__':
    app.run()
