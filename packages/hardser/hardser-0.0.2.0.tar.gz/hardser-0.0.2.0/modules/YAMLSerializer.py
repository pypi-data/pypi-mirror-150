from modules.Serializer import Serializer
from modules.hard_tools import ser
from modules.hard_tools import des
import yaml


class YamlSerializer(Serializer):
    def dump(self, obj, fp: str):
        ser_obj = self.dumps(obj)
        try:
            with open(fp, 'w') as f:
                f.write(ser_obj)
        except IOError:
            print("An IOError has occurred!")
        return ser_obj

    def dumps(self, obj):
        yaml_obj = change_tuple_to_list(ser(obj))
        # yaml = func_convert(yaml_obj)
        return yaml.dump(yaml_obj)

    def load(self, fp):
        try:
            with open(fp, 'r') as f:
                script = f.read()
        except IOError:
            print(f"An IOError has occurred: failed to open {fp}")
            return
        return self.loads(script)

    def loads(self, s):
        obj = dict()
        try:
            obj = yaml.safe_load(s)
            obj = change_key_from_not_tuple(obj)
        except yaml.YAMLError as exc:
            print(exc)
        return des(obj)

    '''def dumps(self, obj: object, dumper=yaml.Dumper):
        return yaml.dumps(ser(obj), Dumper=dumper)

    def dump(self, obj: object, fp: str, dumper=yaml.Dumper):
        with open(fp, "w") as file:
            file.write(self.dumps(obj, dumper=dumper))

    def loads(self, data: str, loader=yaml.FullLoader):
        return from_dict(yaml.load(data, Loader=loader))

    def load(self, fp: str, loader=yaml.FullLoader):
        with open(fp, "r") as file:
            return self.loads(file.read(), loader=loader)'''


TYPES = ["list", "tuple", "bytes", "dict",
         'co_argcount',
         'co_posonlyargcount',
         'co_kwonlyargcount',
         'co_nlocals',
         'co_stacksize',
         'co_flags',
         'co_code',
         'co_consts',
         'co_names',
         'co_varnames',
         'co_filename',
         'co_name',
         'co_firstlineno',
         'co_lnotab',
         'co_freevars',
         'co_cellvars',
         '__name__',
         '__globals__',
         '__func__',
         '__args__',
         '__builtins__',
         '__class__',
         '__object__']


def change_key_from_not_tuple(obj, flag=False):
    dc = obj.copy()
    for k, v in obj.items():
        copy = k
        if k not in TYPES and flag:
            copy = [(k, v) for k, v in ser(k).items()][0]
            dc[copy] = dc.pop(k)
        if isinstance(v, dict):
            dc[copy] = change_key_from_not_tuple(v, k == "dict")
    return dc


def change_tuple_to_list(obj):
    dt = obj.copy()
    for k, v in obj.items():
        if isinstance(v, dict):
            dt[k] = change_tuple_to_list(v)
        if k == "tuple" or k == "list" or k == "bytes":
            copy = []
            for it in list(v):
                copy.append(change_tuple_to_list(it))
            dt[k] = copy
        if isinstance(k, tuple):
            dt[k[1]] = dt.pop(k)
    return dt


'''def func_convert(obj):
    if "__func__" in obj.keys() and obj["__func__"]["__name__"] in obj["__func__"]["__globals__"].keys():
        if obj["__name__"] in obj["__globals__"]:
            flag = True'''
