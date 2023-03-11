from werkzeug.security import generate_password_hash

from models.user import User
from repository.repository import Repository


class UserRepository(Repository):
    def __init__(self, folder, filename='users.csv', delimiter=';'):
        super().__init__(folder, filename, delimiter)

        users = self.find_all()

        if len(users) == 0:
            user = User(None, 'admin', 'admin', True)
            user.password = generate_password_hash(user.password)
            self.save(user)

    def load_by_username(self, username):
        users = self.find_all()

        for user in users:
            if user.username == username:
                return user

        return None

    def _get_header(self):
        return 'id' \
            + self.delimiter + 'name' \
            + self.delimiter + 'password' \
            + self.delimiter + 'role'

    def _line_to_entity(self, line):
        line = line.strip()
        values = line.split(self.delimiter)

        if len(values) >= 4:
            return User(int(values[0]), values[1].strip(), values[2].strip(), values[3].strip().upper() == 'ADMIN')
        elif len(values) >= 3:
            return User(None, values[0].strip(), values[1].strip(), values[2].strip().upper() == 'ADMIN')
        else:
            return User(None, values[0].strip(), values[1].strip())

    def _entity_to_line(self, user):
        return str(user.user_id) \
            + self.delimiter + user.username \
            + self.delimiter + user.password \
            + self.delimiter + ('ADMIN' if user.admin else 'USER')
