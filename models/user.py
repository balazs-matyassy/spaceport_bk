class User:
    def __init__(self, user_id, username, password, admin=False):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.admin = admin

    @staticmethod
    def create_header(delimiter=';'):
        return 'id' \
            + delimiter + 'name' \
            + delimiter + 'password' \
            + delimiter + 'role'

    @staticmethod
    def create_from_line(line, delimiter=';'):
        line = line.strip()
        values = line.split(delimiter)

        if len(values) >= 4:
            return User(int(values[0]), values[1].strip(), values[2].strip(), values[3].strip().upper() == 'ADMIN')
        elif len(values) >= 3:
            return User(None, values[0].strip(), values[1].strip(), values[2].strip().upper() == 'ADMIN')
        else:
            return User(None, values[0].strip(), values[1].strip())

    def to_line(self, delimiter=';'):
        return str(self.user_id) \
            + delimiter + self.username \
            + delimiter + self.password \
            + delimiter + ('ADMIN' if self.admin else 'USER')
