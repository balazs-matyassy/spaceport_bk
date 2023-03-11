from models.category import Category
from repository.repository import Repository


class CategoryRepository(Repository):
    def __init__(self, db, table='category'):
        super().__init__(db, table)

    def _row_to_entity(self, row):
        return Category(row['id'], row['name'])

    def _create(self, category):
        category.category_id = self.db.execute(f"""
            INSERT INTO {self.table} (name)
            VALUES (?)
        """, (category.name,)).lastrowid
        self.db.commit()

        return category

    def _update(self, category):
        rowcount = self.db.execute(f"""
            UPDATE {self.table} SET
                name = ?
            WHERE id = ?
        """, (category.name, category.category_id)).rowcount

        if rowcount == 1:
            self.db.commit()
            return category
        else:
            return None
