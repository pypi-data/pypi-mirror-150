from modules.SerializeCreate import Creator
from modules.Serializer import Serializer
from modules.TOMLSerializer import TomlSerializer


class TomlSerializerCreator(Creator):
    def create_serializer(self) -> Serializer:
        return TomlSerializer()
