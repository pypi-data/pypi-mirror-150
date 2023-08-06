from abc import ABC, abstractmethod


class Creator(ABC):
    @abstractmethod
    def create_serializer(self):
        pass
