from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash

from auth import admin_granted
from db import get_user_repository
from models.user import User

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route('/')
@admin_granted
def users_list():
    user_repository = get_user_repository()
    users = user_repository.load_all()
    return render_template('users/list.html', users=users)


@bp.route('/create', methods=("GET", "POST"))
@admin_granted
def users_create():
    user = User(None, '', '')

    if request.method == "POST":
        user.username = request.form['username']
        user.password = request.form['password']
        user.admin = request.form['role'] == 'ADMIN'

        if user.username != '' and user.password != '':
            user.password = generate_password_hash(user.password)

            user_repository = get_user_repository()
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


@bp.route('/<int:user_id>/edit', methods=("GET", "POST"))
@admin_granted
def users_edit(user_id):
    user_repository = get_user_repository()
    user = user_repository.load_by_id(user_id)

    if request.method == "POST":
        user.username = request.form['username']

        if user.username != '':
            if request.form['password'] != '':
                user.password = generate_password_hash(request.form['password'])

            user.admin = request.form['role'] == 'ADMIN'
            user_repository.save(user)
            flash('User saved.')
        else:
            flash('Username missing.')

    return render_template(
        'users/edit.html',
        create=False,
        user=user
    )


@bp.route('/<int:user_id>/delete', methods=["POST"])
@admin_granted
def users_delete(user_id):
    user_repository = get_user_repository()
    user_repository.delete(user_id)
    flash('User deleted.')

    return redirect(url_for("users_list"))
