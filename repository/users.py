from werkzeug.security import generate_password_hash

from models.user import User
from repository.repository import Repository


class UserRepository(Repository):
    def __init__(self, folder, filename='users.csv', delimiter=';'):
        super().__init__(User, folder, filename, delimiter)

        users = self.load_all()

        if len(users) == 0:
            user = User(None, 'admin', 'admin', True)
            user.password = generate_password_hash(user.password)
            self.save(user)

    def load_by_username(self, username):
        users = self.load_all()

        for user in users:
            if user.username == username:
                return user

        return None
