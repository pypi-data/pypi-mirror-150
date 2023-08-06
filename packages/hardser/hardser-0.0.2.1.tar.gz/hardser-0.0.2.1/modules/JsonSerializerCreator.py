from modules.SerializeCreate import Creator
from modules.Serializer import Serializer
from modules.JsonSerializer import JsonSerializer


class JsonSerializerCreator(Creator):
    def create_serializer(self) -> Serializer:
        return JsonSerializer()
