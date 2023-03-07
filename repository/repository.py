import os


class Repository:
    def __init__(self, model_class, folder, filename, delimiter=';'):
        self.model_class = model_class
        self.path = os.path.join(folder, filename)
        self.delimiter = delimiter

        os.makedirs(folder, exist_ok=True)

        if not os.path.isfile(self.path):
            with open(self.path, 'w', encoding='utf-8') as file:
                header = self.model_class.create_header(self.delimiter)
                file.write(f'{header}\n')

    def load_all(self):
        entities = []

        with open(self.path, encoding='utf-8') as file:
            file.readline()

            for line in file:
                entity = self.model_class.create_from_line(line, self.delimiter)
                entities.append(entity)

            return entities

    def save_all(self, entities):
        with open(self.path, 'w', encoding='utf-8') as file:
            header = self.model_class.create_header(self.delimiter)
            file.write(f'{header}\n')

            for entity in entities:
                line = entity.to_line(self.delimiter)
                file.write(f'{line}\n')

    def load_by_id(self, entity_id):
        entities = self.load_all()

        for entity in entities:
            if entity.get_id() == entity_id:
                return entity

        return None

    def save(self, entity):
        if entity.get_id() is None:
            # CREATE
            return self.__create(entity)
        else:
            # UPDATE
            return self.__update(entity)

    def delete(self, entity_id):
        entities = self.load_all()
        filtered = []
        deleted_entity = None

        for entity in entities:
            if entity.get_id() != entity_id:
                filtered.append(entity)
            else:
                deleted_entity = entity

        if deleted_entity is not None:
            self.save_all(filtered)

        return deleted_entity

    def __create(self, entity):
        entities = self.load_all()
        max_id = 0

        for stored_entity in entities:
            if stored_entity.get_id() > max_id:
                max_id = stored_entity.get_id()

        entity.set_id(max_id + 1)

        with open(self.path, 'a', encoding='utf-8') as file:
            line = entity.to_line(self.delimiter)
            file.write(f'{line}\n')

        return entity

    def __update(self, entity):
        entities = self.load_all()
        updated_entity = None

        for i in range(len(entities)):
            if entities[i].get_id() == entity.get_id():
                entities[i] = entity
                updated_entity = entities[i]
                break

        if updated_entity is not None:
            self.save_all(entities)

        return updated_entity
