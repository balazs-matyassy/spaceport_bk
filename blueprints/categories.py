from flask import Blueprint, render_template, request, flash, redirect, url_for

from auth import fully_authenticated
from db import get_category_repository
from models.category import Category

bp = Blueprint('categories', __name__, url_prefix="/categories")


@bp.route('/')
def categories_list():
    category_repository = get_category_repository()
    categories = category_repository.load_all()
    return render_template('categories/list.html', categories=categories)


@bp.route('/create', methods=("GET", "POST"))
@fully_authenticated
def categories_create():
    category = Category(None, '')

    if request.method == "POST":
        category.name = request.form['name']
        category_repository = get_category_repository()
        category_repository.save(category)

        flash('Category created.')

        return redirect(url_for("categories.categories_list"))

    return render_template(
        'categories/edit.html',
        create=True,
        category=category
    )


@bp.route('/<int:category_id>/edit', methods=("GET", "POST"))
@fully_authenticated
def categories_edit(category_id):
    category_repository = get_category_repository()
    category = category_repository.load_by_id(category_id)

    if request.method == "POST":
        category.name = request.form['name']
        flash('Category saved.')

    return render_template(
        'categories/edit.html',
        create=False,
        category=category
    )


@bp.route('/<int:category_id>/delete', methods=["POST"])
@fully_authenticated
def categories_delete(category_id):
    category_repository = get_category_repository()
    category_repository.delete(category_id)
    flash('Category deleted.')

    return redirect(url_for("categories.categories_list"))
