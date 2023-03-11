from models.entity import Entity


class Category(Entity):
    def __init__(self, category_id, name):
        self.category_id = category_id
        self.name = name

    def get_id(self):
        return self.category_id

    def set_id(self, entity_id):
        self.category_id = entity_id
