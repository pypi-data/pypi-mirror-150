import argparse

from modules.JsonSerializerCreator import JsonSerializerCreator
from modules.TOMLSerializerCreator import TomlSerializerCreator
from modules.YAMLSerializerCreator import YamlSerializerCreator

parser = argparse.ArgumentParser(description='Process converting between formats.')
parser.add_argument('-source', dest='source', type=str,
                    help='source file path')
parser.add_argument('-source_format', dest='source_format', type=str,
                    help='source format')
parser.add_argument('-destination', dest='destination', type=str,
                    help='destination file path')
parser.add_argument('-format', dest='format', type=str,
                    help='new format')
parser.add_argument('-conf_file', dest="conf_file", type=str,
                    help='configuration file')

formats = {'JSON': JsonSerializerCreator(), 'YAML': YamlSerializerCreator(), 'TOML': TomlSerializerCreator()}


def setup():
    args = parser.parse_args()
    source = args.source
    source_format = args.source_format
    destination = args.destination
    format = args.format
    if args.conf_file is not None and args.conf_file is "config.py":
        config = __import__(args.conf_file)
        flag = False

        if hasattr(config, "source"):
            source = config.source
        else:
            flag = True

        if hasattr(config, "source_format"):
            source_format = config.source_format
        else:
            flag = True

        if hasattr(config, "destination"):
            destination = config.destination
        else:
            flag = True

        if hasattr(config, "format"):
            format = config.format
        else:
            flag = True

        if not flag:
            convert(source, source_format, destination, format)
    else:
        convert(source, source_format, destination, format)


def convert(source, source_format, dest, dest_format):
    if dest_format.upper() not in formats.keys():
        raise ValueError('Invalid format')

    try:
        with open(source, 'r') as src:
            if source_format.upper() not in formats.keys():
                raise ValueError(f'File should contain a format: {formats.keys()}')
            if source_format.upper() != dest_format.upper():
                source_serializer = formats[source_format.upper()].create_serializer()
                serializer = formats[dest_format.upper()].create_serializer()
                with open(dest, 'w') as dst:
                    data = source_serializer.loads(src.read())
                    dst.write(serializer.dumps(data))
            else:
                raise ValueError(f'Source and destination format shouldn\'t be same')
    except IOError:
        print(f"Can't open file: {source}")


if __name__ == "__main__":
    setup()
