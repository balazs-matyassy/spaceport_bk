from abc import abstractmethod


class Model:
    @abstractmethod
    def get_id(self):
        raise NotImplementedError

    @abstractmethod
    def set_id(self, entity_id):
        raise NotImplementedError

    @abstractmethod
    def to_line(self, delimiter=';'):
        raise NotImplementedError
