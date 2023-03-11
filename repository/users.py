from werkzeug.security import generate_password_hash

from models.user import User

from repository.repository import Repository


class UserRepository(Repository):
    def __init__(self, db, table='user'):
        super().__init__(db, table)

    def find_one_by_username(self, username):
        query = f"""
            SELECT *
            FROM {self.table}
            WHERE username = ?
        """

        return self._find_one_by_query(query, (username,))

    def _row_to_entity(self, row):
        return User(row['id'], row['username'], row['password'], row['role'].strip().upper() == 'ADMIN')

    def _create(self, user):
        user.user_id = self.db.execute(f"""
            INSERT INTO {self.table} (username, password, role)
            VALUES (?, ?, ?)
        """, (user.username, user.password, 'ADMIN' if user.admin else 'USER')).lastrowid
        self.db.commit()

        return user

    def _update(self, user):
        rowcount = self.db.execute(f"""
            UPDATE {self.table} SET
                username = ?,
                password = ?,
                role = ?
            WHERE id = ?
        """, (user.username, user.password, 'ADMIN' if user.admin else 'USER', user.user_id)).rowcount

        if rowcount == 1:
            self.db.commit()
            return user
        else:
            return None
