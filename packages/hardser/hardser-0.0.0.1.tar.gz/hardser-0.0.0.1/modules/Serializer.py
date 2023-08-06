from abc import ABC, abstractmethod


class Serializer(ABC):
    @abstractmethod
    def dump(self, obj, file):
        pass

    @abstractmethod
    def dumps(self, obj):
        pass

    @abstractmethod
    def load(self, file):
        pass

    @abstractmethod
    def loads(self, s):
        pass