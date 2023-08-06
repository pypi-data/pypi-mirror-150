import argparse
import re

from modules.JsonSerializerCreator import JsonSerializerCreator
from modules.TOMLSerializerCreator import TomlSerializerCreator
from modules.YAMLSerializerCreator import YamlSerializerCreator

parser = argparse.ArgumentParser(description='Process converting between formats.')
parser.add_argument('-s', dest='source', type=str,
                    help='source file path')
parser.add_argument('-sf', dest='source_format', type=str,
                    help='source format')
parser.add_argument('-d', dest='destination', type=str,
                    help='destination file path')
parser.add_argument('-df', dest='format', type=str,
                    help='new format')
parser.add_argument('-cf', dest="conf_file", type=str,
                    help='configuration file')

formats = {'JSON': JsonSerializerCreator(), 'YAML': YamlSerializerCreator(), 'TOML': TomlSerializerCreator()}


def setup():
    args = parser.parse_args()
    source = args.source
    source_format = args.source_format
    destination = args.destination
    des_format = args.format
    if args.conf_file is not None:  # and args.conf_file == "config.py"
        data = {}
        try:
            with open(args.conf_file, 'r') as cf:
                for line in cf:
                    line = line.replace("\n", "")
                    (key, value) = re.findall(r"[^= \"\']+", line)
                    data[key] = value
        except IOError as e:
            print(e)

        flag = False

        if "source" in data.keys():
            source = data["source"]
        else:
            flag = True

        if "source_format" in data.keys():
            source_format = data["source_format"]
        else:
            flag = True

        if "destination" in data.keys():
            destination = data["destination"]
        else:
            flag = True

        if "format" in data.keys():
            des_format = data["format"]
        else:
            flag = True

        if not flag:
            convert(source, source_format.upper(), destination, des_format.upper())
        else:
            raise ValueError(f'Not correct config file: {formats.keys()}')

    else:
        convert(source, source_format.upper(), destination, des_format.upper())


def convert(source: str, source_format: str, destination: str, des_format):
    if des_format not in formats.keys():
        raise ValueError('Invalid format')

    try:
        with open(source, 'r') as src:
            if source_format not in formats.keys():
                raise ValueError(f'File should contain a format: {formats.keys()}')
            if source_format != des_format:
                print(f'From {source}({source_format})...')
                source_serializer = formats[source_format].create_serializer()
                serializer = formats[des_format].create_serializer()
                with open(destination, 'w') as dst:
                    data = source_serializer.loads(src.read())
                    dst.write(serializer.dumps(data))
                    print(f'To {destination}({des_format})      Completed!')
            else:
                raise ValueError(f'Source and destination format shouldn\'t be same')
    except IOError:
        print(f"Can't open file: {source}")


if __name__ == "__main__":
    setup()
