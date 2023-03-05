import os

from werkzeug.security import generate_password_hash

from models.user import User


class UserRepository:
    def __init__(self, folder, filename='users.csv', delimiter=';'):
        os.makedirs(folder, exist_ok=True)

        self.path = os.path.join(folder, filename)
        self.delimiter = delimiter

        if not os.path.isfile(self.path):
            with open(self.path, 'w', encoding='utf-8') as file:
                header = User.create_header(self.delimiter)
                user = User(1, 'admin', 'admin', True)
                user.password = generate_password_hash(user.password)
                line = user.to_line(self.delimiter)

                file.write(f'{header}\n')
                file.write(f'{line}\n')

    def load_all(self):
        users = []

        with open(self.path, encoding='utf-8') as file:
            file.readline()

            for line in file:
                user = User.create_from_line(line, self.delimiter)
                users.append(user)

            return users

    def save_all(self, users):
        with open(self.path, 'w', encoding='utf-8') as file:
            header = User.create_header(self.delimiter)
            file.write(f'{header}\n')

            for user in users:
                line = user.to_line(self.delimiter)
                file.write(f'{line}\n')

    def load_by_id(self, user_id):
        users = self.load_all()

        for user in users:
            if user.user_id == user_id:
                return user

        return None

    def load_by_username(self, username):
        users = self.load_all()

        for user in users:
            if user.username == username:
                return user

        return None

    def save(self, user):
        if user.user_id is None:
            # CREATE
            return self.__create(user)
        else:
            # UPDATE
            return self.__update(user)

    def delete(self, user_id):
        users = self.load_all()
        filtered = []
        deleted_user = None

        for user in users:
            if user.user_id != user_id:
                filtered.append(user)
            else:
                deleted_user = user

        if deleted_user is not None:
            self.save_all(filtered)

        return deleted_user

    def __create(self, user):
        users = self.load_all()
        max_id = 0

        for stored_user in users:
            if stored_user.user_id > max_id:
                max_id = stored_user.user_id

        user.user_id = max_id + 1

        with open(self.path, 'a', encoding='utf-8') as file:
            line = user.to_line(self.delimiter)
            file.write(f'{line}\n')

        return user

    def __update(self, user):
        users = self.load_all()
        updated_user = None

        for stored_user in users:
            if stored_user.user_id == user.user_id:
                stored_user.username = user.username
                stored_user.password = user.password
                stored_user.admin = user.admin
                updated_user = stored_user
                break

        if updated_user is not None:
            self.save_all(users)

        return updated_user
