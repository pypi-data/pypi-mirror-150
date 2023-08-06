import builtins
import inspect
from types import FunctionType, CodeType, LambdaType


def ser(obj):  # serialize
    return pre_ser(obj)


def pre_ser(obj):
    if isinstance(obj, (int, float, str, bool, type(None))):
        return basic_type_ser(obj)
    elif isinstance(obj, (list, tuple, bytes)):
        return tl_ser(obj)
    elif isinstance(obj, dict):
        return dict_ser(obj)
    elif inspect.iscode(obj):
        return ser_func(FunctionType(obj, {}))
    elif inspect.isfunction(obj) or inspect.ismethod(obj) or isinstance(obj, LambdaType):
        return ser_func(obj)
    elif inspect.isclass(obj):
        return ser_class(obj)
    elif inspect.isbuiltin(obj):
        return serialize_prop(obj)
    else:
        return ser_obj(obj)
        # return serialize_prop(obj)


def basic_type_ser(obj):  # str & None & bool & int & float
    temp_dict = dict()
    if isinstance(obj, str):
        temp_dict["str"] = obj
    elif isinstance(obj, type(None)):
        temp_dict["None"] = obj
    elif isinstance(obj, bool):
        temp_dict["bool"] = obj
    elif isinstance(obj, int):
        temp_dict["int"] = obj
    elif isinstance(obj, float):
        temp_dict["float"] = obj
    return temp_dict


def tl_ser(obj):  # tuple & list $ bytes
    temp_dict = dict()
    if isinstance(obj, list):
        m_key = "list"
        temp_dict["list"] = tuple(ser(el) for el in obj)
    elif isinstance(obj, tuple):
        m_key = "tuple"
        temp_dict["tuple"] = tuple(ser(el) for el in obj)
    else:
        m_key = "bytes"
        temp_dict["bytes"] = tuple(ser(el) for el in obj)
    return temp_dict


def dict_ser(obj):
    temp_dict = dict()
    temp_dict["dict"] = {}
    for k, v in obj.items():
        temp = pre_ser(k)  # bbbbbbrrrrrrrrr
        for kk, vv in temp.items():  # get just one key_type: key_value
            key = tuple((kk, vv))
            temp_dict["dict"][key] = pre_ser(v)
    return temp_dict


'''def serialize_code(obj):
    main_key = "code"
    ans = dict()
    ans[main_key] = {}

    attr = inspect.getmembers(obj)
    attr = [i for i in attr if not callable(i[1])]
    for i in attr:
        key = ser(i[0])
        val = ser(i[1])
        ans[main_key][ser(i[0])] = ser(i[1])
    ans[main_key] = tuple((k, ans[main_key][k]) for k in ans[main_key])

    return ans'''


'''def serialize_function(obj):
    FAT = [  # Function ATtr.
        "__code__",
        "__name__",
        "__defaults__",
        "__closure__",
        "__dir__",
        "__format__"
    ]
    main_key = "function"
    ans = dict()
    ans[main_key] = {}
    attr = inspect.getmembers(obj)
    attr = [i for i in attr if i[0] in FAT]
    for i in attr:
        key = ser(i[0])
        value = ser(i[1])
        ans[main_key][ser(i[0])] = ser(i[1])
        # key = pre_ser(i[0])
        # value = pre_ser(i[1])
        # if i[0] != "__closure__":
        # else:
        #    value = pre_ser(None)

        if i[0] == "__code__":
            key = ser("__globals__")
            ans[main_key][key] = {}
            names = i[1].__getattribute__("co_names")
            glob = obj.__getattribute__("__globals__")
            glob_dict = {}
            for name in names:
                if name == obj.__name__:
                    glob_dict[name] = obj.__name__
                elif name in glob and not inspect.ismodule(name) and name not in __builtins__:
                    glob_dict[name] = glob[name]
            ans[main_key][key] = ser(glob_dict)

    ans[main_key] = tuple((k, ans[main_key][k]) for k in ans[main_key])
    return ans'''


'''def nesting(level: int) -> str:
    result = ""
    for i in range(level):
        result += "\t"
    return result'''


def serialize_prop(obj):
    return {"str": f"{obj}"}


def glob_variables(func):
    gl_vars = {}
    for current_gl in func.__code__.co_names:  # search in used global variables
        if current_gl in func.__globals__:  # check if they are visible
            if inspect.isfunction(func.__globals__[current_gl]) and func.__globals__[current_gl].__name__ == func.__name__:
                gl_vars[current_gl] = str(func)  # str
            else:
                gl_vars[current_gl] = pre_ser(func.__globals__[current_gl])  # pre_ser(func.__globals__[current_gl])
    return gl_vars


# {
#   "__func__" :
#       {
#       "__name__": obj.__name,
#       "__globals__": {{:}, ...},
#       "__args__": {{:}, ...},
#       }
# }
def ser_func(obj):
    if inspect.ismethod(obj):
        obj = obj.__func__
    output = dict()
    args = dict()
    cycle = [c for c in obj.__code__.__dir__() if c.startswith('co_')]
    for c in cycle:
        attr = getattr(obj.__code__, c)
        # if isinstance(attr, bytes):
            # attr = pre_ser(attr)  # test
            # attr = attr.decode('raw_unicode_escape')
        if isinstance(attr, (list, tuple, dict)):
            converted_vals = []
            for val in attr:
                converted_vals.append(val)  # pre_ser val
            args[c] = pre_ser(converted_vals)  # pre_ser
            continue
        args[c] = pre_ser(attr)

    m_key = "__func__"
    output[m_key] = {"__name__": obj.__name__,
                     "__globals__": glob_variables(obj),
                     "__args__": args}

    return output


# {
#   "__object__" :
#       {
#       "__name__": class.__name__,
#       "__attrs__": {{:}, ...},
#       }
# }
def ser_obj(obj):
    out_attrs = dict()
    m_key = "__object__"
    cycle = [i for i in dir(obj) if not i.startswith("__")]
    for attr in cycle:
        out_attrs[attr] = pre_ser(getattr(obj, attr))
    output = {m_key: {"__name__": obj.__class__.__name__,
                      "__attrs__": out_attrs}}
    return output


# {
#   "__class__" :
#       {
#       "__name__": obj.__name__,
#       "__attrs__": {{:}, ...},
#       }
# }
def ser_class(obj):
    output = dict()
    out_attrs = dict()
    m_key = "__class__"
    attrs = [i for i in dir(obj) if not i.startswith('__') or inspect.isfunction(getattr(obj, i))]
    for attr in attrs:
        attr_value = getattr(obj, attr)
        out_attrs[attr] = pre_ser(attr_value)

    output[m_key] = {'__name__': obj.__name__,
                     '__attrs__': out_attrs}
    return output


SIMPLE_TYPES = ["str", "int", "float", "bool", "None"]
L_T_B_TYPES = ["list", "tuple", "bytes"]


def des(obj):
    for k, v in obj.items():
        if k in SIMPLE_TYPES:
            return des_types(v)
        elif k in L_T_B_TYPES:
            return des_ltb(k, v)
        elif k == "dict":
            return des_dict(v)
        elif k == "__func__":
            return des_func(v)
        elif k == "__class__":
            return des_class(v)
        elif k == "__object__":
            return des_obj(v)


def des_types(obj):
    return obj


def des_ltb(tp, obj):
    output = []
    for el in obj:
        output.append(des(el))

    if tp == "tuple":
        output = tuple(output)
    elif tp == "bytes":
        output = bytes(output)
    return output


def des_dict(obj):
    output = dict()
    for k, v in obj.items():
        key = des({k[0]: k[1]})
        output[key] = des(v)

    return output


def des_func(obj):
    flag = False
    args = obj["__args__"]
    if "__globals__" not in obj.keys():
        obj["__globals__"] = {}
    globs = obj["__globals__"]
    if obj["__name__"] in globs.keys():
        flag = True
    globs["__builtins__"] = builtins
    for key in obj["__globals__"]:
        if len(args["co_names"]) != 0 and key in des(args["co_names"]):  # list
            if key != des(args["co_name"]):
                globs[key] = des(obj["__globals__"][key])

    for k, v in args.items():
        if k == "co_consts":
            consts = []
            for val in des(args["co_consts"]):
                if inspect.isfunction(val) or inspect.ismethod(val) or isinstance(val, LambdaType):
                    # val = des(val)
                    consts.append(val.__code__)
                    continue
                consts.append(val)
            args[k] = consts
        else:
            args[k] = des(args[k])

    code = CodeType(args['co_argcount'],
                    args['co_posonlyargcount'],
                    args['co_kwonlyargcount'],
                    args['co_nlocals'],
                    args['co_stacksize'],
                    args['co_flags'],
                    bytes(args['co_code']),  # , 'raw_unicode_escape'
                    tuple(args['co_consts']),
                    tuple(args['co_names']),
                    tuple(args['co_varnames']),
                    args['co_filename'],
                    args['co_name'],
                    args['co_firstlineno'],
                    bytes(args['co_lnotab']),  # , 'raw_unicode_escape'
                    tuple(args['co_freevars']),
                    tuple(args['co_cellvars']))
    output = FunctionType(code, globs)
    # print(output.__globals__)
    if flag:
        output.__globals__[obj["__name__"]] = output
    # print(output.__globals__)
    return output


def des_obj(obj):
    '''dct = {}
    output = type(obj["__name__"], (), {})
    attrs = obj["__attrs__"]
    for i in attrs:
        # dct[i] = des(attrs[i])
        setattr(output, i, des(attrs[i]))
    return output'''
    # return type(obj["__name__"], (), dct)
    dct = {}
    # res = type(obj["__name__"], (), {})
    attrs = obj["__attrs__"]
    func = []
    for i in attrs:
        ob = des(attrs[i])
        if inspect.isfunction(ob) and "self" in ob.__code__.co_varnames:
            func.append(ob)
        else:
            dct[i] = ob
    output = type(obj["__name__"], (), dct)
    for i in func:
        setattr(output, i.__name__, i.__get__(output))
        # name = i.__name__
        # output.name = i.__get__(output)
    return output
    # return type(obj["__name__"], (), dct)


def des_class(obj):
    dct = {}
    attrs = obj["__attrs__"]
    # for i in attrs:
    #    dct[i] = des(attrs[i])

    func = []
    for i in attrs:
        ob = des(attrs[i])
        if inspect.isfunction(ob) and "self" in ob.__code__.co_varnames:
            func.append(ob)
        else:
            dct[i] = ob
    output = type(obj["__name__"], (), dct)
    for i in func:
        setattr(output, i.__name__, i.__get__(output))
        # name = i.__name__
        # output.name = i.__get__(output)
    return output

    # for attr, val in obj.items():
    #    if attr != "__name__":
    #        dct[attr] = des(val)
    # return type(obj["__name__"], (), dct)


'''def serialize_instance(instance_obj):
    ans = dict()
    type = re.search(r"\'(\w+)\'", str(type(instance_obj))).group(1)
    ans[type] = {}
    members = inspect.getmembers(instance_obj)
    members = [i for i in members if not callable(i[1])]
    for i in members:
        key = ser(i[0])
        val = ser(i[1])
        ans[type][key] = val
    ans[type] = tuple((k, ans[type][k]) for k in ans[type])

    return ans'''

