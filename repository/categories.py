from models.category import Category
from repository.repository import Repository


class CategoryRepository(Repository):
    def __init__(self, folder, filename='categories.csv', delimiter=';'):
        super().__init__(Category, folder, filename, delimiter)
