import unittest
from modules.SerFactory import ParserFactory


def add(c, y):
    return c + y


def factor(f):
    if f > 1:
        return f * factor(f - 1)
    else:
        return f


mul = lambda c, y: c * y


def decor():
    def beb():
        return "fff"

    return beb


x = 50


class MyClass:
    class_v = 10

    def __init__(self):
        print("ggg")

    def cl(self, y):
        return x * (self.class_v - y)

    @staticmethod
    def br(y):
        return y * y


class MyCl(MyClass):
    class_b = 11

    def bruh(self):
        print(f"OH MY GOD {self.class_b}")


my_obj = MyClass()


class TestFunc(unittest.TestCase):
    format = {"json": "test_json.json", "toml": "test_toml.toml", "yaml": "test_yaml.yaml"}

    def test_str_one(self):
        for val in self.format.keys():
            parser = ParserFactory.create_parser(val)
            in_format = parser.dumps(add)
            in_python = parser.loads(in_format)
            self.assertEqual(in_python(1, 2), add(1, 2))

    def test_str_two(self):
        for val in self.format.keys():
            parser = ParserFactory.create_parser(val)
            in_format = parser.dumps(decor)
            in_python = parser.loads(in_format)
            test_func = in_python()
            real_func = decor()
            self.assertEqual(test_func(), real_func())

    def test_file(self):
        for k, v in self.format.items():
            parser = ParserFactory.create_parser(k)
            parser.dump(add, v)
            in_python = parser.load(v)
            self.assertEqual(in_python(2, -2), add(2, -2))

    def test_factor(self):
        for val in self.format.keys():
            parser = ParserFactory.create_parser(val)
            in_format = parser.dumps(factor)
            in_python = parser.loads(in_format)
            parsed = in_python
            real = factor
            self.assertEqual(parsed(4), real(4))

    def test_error_file(self):
        v = "error.txt"
        for k in self.format.keys():
            parser = ParserFactory.create_parser(k)
            self.assertEqual(parser.load(v), None)
            # with self.assertRaises(IOError) as cm:
            #    pass
            # self.assertRaises(IOError, parser.dump(add, v))

    def test_lambda(self):
        for val in self.format.keys():
            parser = ParserFactory.create_parser(val)
            in_format = parser.dumps(mul)
            in_python = parser.loads(in_format)
            self.assertEqual(in_python(4, 3), mul(4, 3))


class TestClass(unittest.TestCase):
    format = {"json": "test_json.json", "toml": "test_toml.toml", "yaml": "test_yaml.yaml"}

    def test_str(self):
        for val in self.format.keys():
            parser = ParserFactory.create_parser(val)
            in_format = parser.dumps(MyClass)
            in_python = parser.loads(in_format)
            self.assertEqual(in_python.br(1), MyClass.br(1))

    def test_file(self):
        for k, v in self.format.items():
            parser = ParserFactory.create_parser(k)
            in_format = parser.dump(MyClass, v)
            in_python = parser.load(v)
            self.assertEqual(in_python.br(1), MyClass.br(1))

    def test_inheritage(self):
        for val in self.format.keys():
            parser = ParserFactory.create_parser(val)
            in_format = parser.dumps(MyCl)
            in_python = parser.loads(in_format)
            obj = in_python()
            self.assertEqual(obj.bruh(), obj.bruh())
            self.assertEqual(in_python.br(15), MyCl.br(15))


class TestObj(unittest.TestCase):
    format = {"json": "test_json.json", "toml": "test_toml.toml", "yaml": "test_yaml.yaml"}

    def test_str(self):
        for val in self.format.keys():
            parser = ParserFactory.create_parser(val)
            in_format = parser.dumps(my_obj)
            in_python = parser.loads(in_format)
            self.assertEqual(in_python.cl(10), my_obj.cl(10))

    def test_file(self):
        for k, v in self.format.items():
            parser = ParserFactory.create_parser(k)
            in_format = parser.dump(my_obj, v)
            in_python = parser.load(v)
            self.assertEqual(in_python.cl(10), my_obj.cl(10))


class TestTypes(unittest.TestCase):
    format = {"json": "test_json.json", "toml": "test_toml.toml", "yaml": "test_yaml.yaml"}

    list = [1, 2, 3, 4, 'abcd']
    tuple = (34, list, dict)
    dict = {"56": (1, 2, 3), 'b': {'c': list}}

    def test_list(self):
        for val in self.format.keys():
            parser = ParserFactory.create_parser(val)
            in_format = parser.dumps(self.list)
            in_python = parser.loads(in_format)
            self.assertEqual(in_python[4], 'abcd')

    def test_dict(self):
        for val in self.format.keys():
            parser = ParserFactory.create_parser(val)
            in_format = parser.dumps(self.dict)
            in_python = parser.loads(in_format)
            self.assertDictEqual(in_python, self.dict)

    def test_tuple(self):
        for val in self.format.keys():
            parser = ParserFactory.create_parser(val)
            in_format = parser.dumps(self.list)
            in_python = parser.loads(in_format)
            self.assertEqual(in_python[4], 'abcd')


if __name__ == "__main__":
    unittest.main()
