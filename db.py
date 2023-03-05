from flask import g, current_app

from repository.products import ProductRepository
from repository.users import UserRepository


def get_user_repository():
    if 'user_repository' not in g:
        g.user_repository = UserRepository(current_app.instance_path)

    return g.user_repository


def get_product_repository():
    if 'product_repository' not in g:
        g.product_repository = ProductRepository(current_app.instance_path)

    return g.product_repository
