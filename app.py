from flask import Flask, render_template, session, g

from blueprints import users, products, login, categories
from db import get_user_repository

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

app.register_blueprint(login.bp)
app.register_blueprint(users.bp)
app.register_blueprint(categories.bp)
app.register_blueprint(products.bp)


@app.before_request
def load_current_user():
    if session.get('user_id') is None:
        g.user = None
    else:
        user_repository = get_user_repository()
        g.user = user_repository.load_by_id(session['user_id'])


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
