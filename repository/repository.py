from abc import abstractmethod


class Repository:
    def __init__(self, db, table):
        self.db = db
        self.table = table

    def find_all(self):
        query = f"""
            SELECT *
            FROM {self.table}
            ORDER BY id
        """

        return self._find_all_by_query(query)

    def find_one_by_id(self, entity_id):
        query = f"""
            SELECT *
            FROM {self.table}
            WHERE id = ?
        """

        return self._find_one_by_query(query, (entity_id,))

    def save(self, category):
        if category.get_id() is None:
            # CREATE
            return self._create(category)
        else:
            # UPDATE
            return self._update(category)

    def delete_by_id(self, entity_id):
        query = f"""
            DELETE FROM {self.table}
            WHERE id = ?
        """
        rowcount = self.db.execute(query, (entity_id,)).rowcount
        self.db.commit()

        return rowcount

    def _find_all_by_query(self, query, params=None):
        if params is not None:
            result = self.db.execute(query, params).fetchall()
        else:
            result = self.db.execute(query).fetchall()

        entities = []

        for row in result:
            entity = self._row_to_entity(row)
            entities.append(entity)

        return entities

    def _find_one_by_query(self, query, params=None):
        if params is not None:
            row = self.db.execute(query, params).fetchone()
        else:
            row = self.db.execute(query).fetchone()

        if row is not None:
            return self._row_to_entity(row)
        else:
            return None

    @abstractmethod
    def _row_to_entity(self, row):
        raise NotImplementedError

    @abstractmethod
    def _create(self, entity):
        raise NotImplementedError

    @abstractmethod
    def _update(self, entity):
        raise NotImplementedError
