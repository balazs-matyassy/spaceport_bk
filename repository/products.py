from models.product import Product
from repository.repository import Repository


class ProductRepository(Repository):
    def __init__(self, db, table='product'):
        super().__init__(db, table)

    def find_all_by_category(self, category_id):
        query = f"""
            SELECT *
            FROM {self.table}
            WHERE category_id = ?
            ORDER BY id
        """

        return self._find_all_by_query(query, (category_id,))

    def delete_by_category(self, category_id):
        query = f"""
            DELETE FROM {self.table}
            WHERE category_id = ?
        """
        rowcount = self.db.execute(query, (category_id,)).rowcount
        self.db.commit()

        return rowcount

    def _row_to_entity(self, row):
        return Product(row['id'], row['category_id'], row['name'], row['unit_price'], row['discount'])

    def _create(self, product):
        product.product_id = self.db.execute(f"""
            INSERT INTO {self.table} (category_id, name, unit_price, discount)
            VALUES (?, ?, ?, ?)
        """, (product.category_id, product.name, product.unit_price, product.discount)).lastrowid
        self.db.commit()

        return product

    def _update(self, product):
        rowcount = self.db.execute(f"""
            UPDATE {self.table} SET
                category_id = ?,
                name = ?,
                unit_price = ?,
                discount = ?
            WHERE id = ?
        """, (product.category_id, product.name, product.unit_price, product.discount, product.product_id)).rowcount

        if rowcount == 1:
            self.db.commit()
            return product
        else:
            return None
