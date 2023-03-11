import os
import sqlite3

import click
from flask import g, current_app

from repository.categories import CategoryRepository
from repository.products import ProductRepository
from repository.users import UserRepository


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    db.commit()


@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Database initialized.')


def get_user_repository():
    if 'user_repository' not in g:
        g.user_repository = UserRepository(get_db())

    return g.user_repository


def get_category_repository():
    if 'category_repository' not in g:
        g.category_repository = CategoryRepository(get_db())

    return g.category_repository


def get_product_repository():
    if 'product_repository' not in g:
        g.product_repository = ProductRepository(get_db())

    return g.product_repository
