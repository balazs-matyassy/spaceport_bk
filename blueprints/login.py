from flask import Blueprint, redirect, url_for, request, session, flash, render_template
from werkzeug.security import check_password_hash

from db import get_user_repository
from models.user import User

bp = Blueprint('login', __name__)


@bp.route('/login', methods=("GET", "POST"))
def login():
    user = User(None, '', '')

    if request.method == "POST":
        user.username = request.form['username']
        user.password = request.form['password']

        user_repository = get_user_repository()
        stored_user = user_repository.find_one_by_username(user.username)

        if stored_user is not None and check_password_hash(stored_user.password, user.password):
            session.clear()
            session['user_id'] = stored_user.user_id
            flash('Login successful.')

            return redirect(url_for('home'))
        else:
            flash('Wrong username or password.')

    return render_template('login/login.html', user=user)


@bp.route('/logout')
def logout():
    session.clear()
    flash('Logout successful.')

    return redirect(url_for('home'))
