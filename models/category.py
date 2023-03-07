from models.model import Model


class Category(Model):
    def __init__(self, category_id, name):
        self.category_id = category_id
        self.name = name

    @staticmethod
    def create_header(delimiter=';'):
        return 'id' \
            + delimiter + 'name'

    @staticmethod
    def create_from_line(line, delimiter=';'):
        line = line.strip()
        values = line.split(delimiter)

        if len(values) >= 2:
            return Category(int(values[0].strip()), values[1].strip())
        else:
            return Category(None, values[0].strip())

    def get_id(self):
        return self.category_id

    def set_id(self, category_id):
        self.category_id = category_id

    def to_line(self, delimiter=';'):
        return str(self.category_id) \
            + delimiter + self.name
