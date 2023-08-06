import re
import sys
from toml.decoder import InlineTableDict
from modules.Serializer import Serializer
from modules.hard_tools import ser
from modules.hard_tools import des
import toml


class TomlSerializer(Serializer):
    def __init__(self):
        toml.TomlEncoder.dump_sections = my_dump_sections

    def dump(self, obj, file: str):
        output = self.dumps(obj)
        with open(file, 'w') as f:
            f.write(output)

    def dumps(self, obj):
        toml_obj = change_tuple_to_list(ser(obj))
        return toml.dumps(toml_obj)

    def load(self, file):
        try:
            with open(file, 'r') as file:
                return self.loads(file.read())
        except IOError:
            print('File IO Error')

    def loads(self, s):
        s = toml.loads(s)
        s = from_toml_obj(s)
        print(s)
        return des(s)


def from_toml_obj(dc):
    dic = dc.copy()
    for k, v in dc.items():
        key = k
        if isinstance(k, str) and k[0] == "(":
            key = str_to_tuple(k)
            dic[key] = dic.pop(k)
        if isinstance(v, dict):  # and len(v) != 1
            dic[key] = from_toml_obj(dic.pop(key))
        if isinstance(v, list):
            dic[key] = from_toml_list(dic.pop(key))
    return dic


def str_to_tuple(s):
    output = list()
    ls = s.split(", ")
    for it in ls:
        el = it
        el = el.replace('(', "")
        el = el.replace(')', "")
        el = el.replace("'", "")
        output.append(el)
    return tuple(output)


def change_tuple_to_list(obj):
    for k, v in obj.items():
        if isinstance(v, dict):
            obj[k] = change_tuple_to_list(v)
        if k == "tuple" or k == "list" or k == "bytes":
            copy_list = list()
            for it in list(v):
                copy_it = it
                if isinstance(it, dict):
                    copy_it = change_tuple_to_list(it)
                copy_list.append(copy_it)
            obj[k] = copy_list
    return obj


def from_toml_list(obj):
    output = list()
    for it in obj:
        copy = it
        if isinstance(it, dict):
            copy = from_toml_obj(it)
        output.append(copy)
    return output


def my_dump_sections(self, o, sup):
    unicode = str
    retstr = ""
    if sup != "" and sup[-1] != ".":
        sup += '.'
    retdict = self._dict()
    arraystr = ""
    for section in o:
        string_repres = unicode(section)  ## MyEdit
        qsection = section
        if not re.match(r'^[A-Za-z0-9_-]+$', string_repres):
            qsection = dump_str(string_repres)
        if not isinstance(o[section], dict):
            arrayoftables = False
            if isinstance(o[section], list):
                for a in o[section]:
                    if isinstance(a, dict):
                        arrayoftables = True
            if arrayoftables:
                for a in o[section]:
                    arraytabstr = "\n"
                    arraystr += "[[" + sup + qsection + "]]\n"
                    s, d = self.dump_sections(a, sup + qsection)
                    if s:
                        if s[0] == "[":
                            arraytabstr += s
                        else:
                            arraystr += s
                    while d:
                        newd = self._dict()
                        for dsec in d:
                            s1, d1 = self.dump_sections(d[dsec], sup +
                                                        qsection + "." +
                                                        dsec)
                            if s1:
                                arraytabstr += ("[" + sup + qsection +
                                                "." + dsec + "]\n")
                                arraytabstr += s1
                            for s1 in d1:
                                newd[dsec + "." + s1] = d1[s1]
                        d = newd
                    arraystr += arraytabstr
            else:
                if o[section] is not None:
                    retstr += (qsection + " = " +
                               unicode(self.dump_value(o[section])) + '\n')
        elif self.preserve and isinstance(o[section], InlineTableDict):
            retstr += (qsection + " = " +
                       self.dump_inline_table(o[section]))
        else:
            retdict[qsection] = o[section]
    retstr += arraystr
    return (retstr, retdict)


def dump_str(v):
    unicode = str
    if sys.version_info < (3,) and hasattr(v, 'decode') and isinstance(v, str):
        v = v.decode('utf-8')
    v = "%r" % v
    if v[0] == 'u':
        v = v[1:]
    singlequote = v.startswith("'")
    if singlequote or v.startswith('"'):
        v = v[1:-1]
    if singlequote:
        v = v.replace("\\'", "'")
        v = v.replace('"', '\\"')
    v = v.split("\\x")
    while len(v) > 1:
        i = -1
        if not v[0]:
            v = v[1:]
        v[0] = v[0].replace("\\\\", "\\")
        # No, I don't know why != works and == breaks
        joinx = v[0][i] != "\\"
        while v[0][:i] and v[0][i] == "\\":
            joinx = not joinx
            i -= 1
        if joinx:
            joiner = "x"
        else:
            joiner = "u00"
        v = [v[0] + joiner + v[1]] + v[2:]
    return unicode('"' + v[0] + '"')

