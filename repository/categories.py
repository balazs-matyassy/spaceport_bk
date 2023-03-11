from models.category import Category
from repository.repository import Repository


class CategoryRepository(Repository):
    def __init__(self, folder, filename='categories.csv', delimiter=';'):
        super().__init__(folder, filename, delimiter)

    def _get_header(self):
        return 'id' \
            + self.delimiter + 'name'

    def _line_to_entity(self, line):
        line = line.strip()
        values = line.split(self.delimiter)

        if len(values) >= 2:
            return Category(int(values[0].strip()), values[1].strip())
        else:
            return Category(None, values[0].strip())

    def _entity_to_line(self, category):
        return str(category.category_id) \
            + self.delimiter + category.name
