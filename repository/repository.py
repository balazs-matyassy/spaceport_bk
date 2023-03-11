import os
from abc import abstractmethod


class Repository:
    def __init__(self, folder, filename, delimiter=';'):
        self.path = os.path.join(folder, filename)
        self.delimiter = delimiter

        os.makedirs(folder, exist_ok=True)

        if not os.path.isfile(self.path):
            with open(self.path, 'w', encoding='utf-8') as file:
                header = self._get_header()
                file.write(f'{header}\n')

    def find_all(self):
        entities = []

        with open(self.path, encoding='utf-8') as file:
            file.readline()

            for line in file:
                entity = self._line_to_entity(line)
                entities.append(entity)

            return entities

    def overwrite(self, entities):
        with open(self.path, 'w', encoding='utf-8') as file:
            header = self._get_header()
            file.write(f'{header}\n')

            for entity in entities:
                line = self._entity_to_line(entity)
                file.write(f'{line}\n')

    def load_one_by_id(self, entity_id):
        entities = self.find_all()

        for entity in entities:
            if entity.get_id() == entity_id:
                return entity

        return None

    def save(self, entity):
        if entity.get_id() is None:
            # CREATE
            return self._create(entity)
        else:
            # UPDATE
            return self._update(entity)

    def delete_by_id(self, entity_id):
        entities = self.find_all()
        filtered = []
        deleted_entity = None

        for entity in entities:
            if entity.get_id() != entity_id:
                filtered.append(entity)
            else:
                deleted_entity = entity

        if deleted_entity is not None:
            self.overwrite(filtered)

        return deleted_entity

    @abstractmethod
    def _get_header(self):
        raise NotImplementedError

    @abstractmethod
    def _line_to_entity(self, line):
        raise NotImplementedError

    @abstractmethod
    def _entity_to_line(self, entity):
        raise NotImplementedError

    def _create(self, entity):
        entities = self.find_all()
        max_id = 0

        for stored_entity in entities:
            if stored_entity.get_id() > max_id:
                max_id = stored_entity.get_id()

        entity.set_id(max_id + 1)

        with open(self.path, 'a', encoding='utf-8') as file:
            line = self._entity_to_line(entity)
            file.write(f'{line}\n')

        return entity

    def _update(self, entity):
        entities = self.find_all()
        updated_entity = None

        for i in range(len(entities)):
            if entities[i].get_id() == entity.get_id():
                entities[i] = entity
                updated_entity = entities[i]
                break

        if updated_entity is not None:
            self.overwrite(entities)

        return updated_entity
