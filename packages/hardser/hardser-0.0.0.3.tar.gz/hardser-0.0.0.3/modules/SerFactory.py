from modules.JsonSerializerCreator import JsonSerializerCreator
from modules.TOMLSerializerCreator import TomlSerializerCreator
from modules.YAMLSerializerCreator import YamlSerializerCreator


class ParserFactory:
    @staticmethod
    def create_parser(name: str):
        name = name.lower()
        if name == "json":
            # parser = ()
            return JsonSerializerCreator().create_serializer()

        if name == "yaml":
            return YamlSerializerCreator().create_serializer()

        if name == "toml":
            return TomlSerializerCreator().create_serializer()

        raise ValueError(f"Format {name} is not supported")
