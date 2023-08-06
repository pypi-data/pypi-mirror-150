from modules.SerializeCreate import Creator
from modules.Serializer import Serializer
from modules.YAMLSerializer import YamlSerializer


class YamlSerializerCreator(Creator):
    def create_serializer(self) -> Serializer:
        return YamlSerializer()