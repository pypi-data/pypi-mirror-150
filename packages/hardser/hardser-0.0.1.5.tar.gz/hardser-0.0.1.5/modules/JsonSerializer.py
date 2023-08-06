from modules.Serializer import Serializer
from modules.hard_tools import ser
from modules.hard_tools import des


class JsonSerializer(Serializer):
    def dump(self, obj, file: str):
        json_str = self.dumps(obj)
        with open(file, 'w') as f:
            f.write(json_str)

    def dumps(self, obj):
        ser_obj = ser(obj)
        return ser_json(ser_obj)

    def load(self, file: str):
        try:
            with open(file, 'r') as f:
                return self.loads(f.read())
        except IOError:
            print('File IO Error')

    def loads(self, s):
        # print(des_json(s))
        return des(des_json(s))


def ser_json(obj) -> str:
    if type(obj) == dict:
        serialized = []
        for k, v in obj.items():
            serialized.append(f"{ser_json(k)}: {ser_json(v)}")
        ans = ", ".join(serialized)
        return f"{{{ans}}}"
    elif type(obj) == tuple or type(obj) == int:
        return str(obj)
    else:
        return f"\'{str(obj)}\'"


def des_json(s: str):
    output = dict()
    for i in range(len(s)):
        if i == 0 and s[i] == "{":
            if s[i + 1] == "}":
                return dict()
            return des_dict(s[1:])
        elif i == 0 and s[i] == "(":
            return find_tuple(s[1:])
        elif i == 0 and s[i] == "\'":
            return search_for_word(s[i + 1:])[0]
        else:
            return s
    return output


def des_dict(s):
    count = 1
    st = ""
    for i in range(len(s)):
        if s[i] == "{":
            count += 1
        elif s[i] == "}":
            if count == 1:
                st = s[:i]
                break
            else:
                count -= 1
    s = st
    output = dict()
    if len(s) == 0:
        return
    while 1:
        key = find_key(s)
        s = go_to_value(s)
        value = des_json(s)
        if key in TYPES:
            value = type_check(key, value)
        output[key] = value
        if isinstance(value, (str, tuple, dict, list)):
            strr = str(value)
            strr = strr.replace("\\\\", "\\")
            s = s[len(strr):]
        s = go_to_next_key(s)
        if len(s) <= 2:
            break
    return output


def go_to_value(s):
    for i in range(1, len(s)):
        if s[i] == ":":
            return s[i + 2:]


def go_to_next_key(s):
    count = 1

    for i in range(0, len(s)):  # 0 1
        if s[i] == ",":
            return s[i + 2:]

    for i in range(1, len(s)):
        if s[i] == "}":
            if count == 1:
                return s[i + 3:]
            else:
                count -= 1
        elif s[i] == "{":
            count += 1
    return ""


def find_key(s):
    if s[0] == "\'":
        for i in range(1, len(s)):
            if s[i] == "\'":
                return s[1:i]
    else:
        return des_json(s)


def find_tuple(s):
    st = ""
    output = []
    count = 1
    for i in range(len(s)):
        if s[i] == "(":
            count += 1
        elif s[i] == ")":
            if count == 1:
                st = s[:i]
                if len(st) == 0:
                    return tuple()
                elif st[0] == "\'":
                    return tuple(get_pair(st[1:len(st)]))
                else:
                    return get_dict_el(st)
            else:
                count -= 1


def get_dict_el(s):
    st = 0
    preout = []
    count = 0
    for i in range(len(s)):
        if s[i] == "{":
            count += 1
            if count == 1:
                st = i
        elif s[i] == "}":
            count -= 1
            if count == 0:
                preout.append(s[st:i + 1])
    output = []
    for i in preout:
        output.append(des_json(i))
    return tuple(output)  # tuple


TYPES = ["str", "int", "bool", "float", "None"]
COLL = ["list", "tuple", "bytes"]


def get_pair(s):
    output = []
    word, ind = search_for_word(s[0:])
    if word in TYPES:
        s = s[ind + 4: len(s) - 1]
        output.append(word)
        output.append(s)
        output[1] = type_check(output[0], output[1])
    else:
        s = s[ind + 2:]
        output.append(des_json(s))
    return output


def search_for_word(s):
    for i in range(len(s)):
        if s[i] == "\'":
            return s[0:i], i


def type_check(tp, v):
    if tp == "int":
        return int(v)
    elif tp == "float":
        return float(v)
    elif tp == "bool":
        return bool(v)
    elif tp == "None":
        return None
    elif tp == "str":
        return v
    else:
        return des_json(v)
