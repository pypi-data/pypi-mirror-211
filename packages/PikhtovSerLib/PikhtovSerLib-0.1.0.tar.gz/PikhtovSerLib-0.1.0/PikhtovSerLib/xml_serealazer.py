from PikhtovSerLib.my_serelizator import Serelizator
from PikhtovSerLib.constants import BASE_TYPES
import regex


class XMLSerelizator:
    key = 'key'
    val = 'value'
    FIND_FOR_XML = fr"\s*(\<(?P<{key}>{BASE_TYPES})\>(?P<{val}>([^<>]*)|(?R)+)\</(?:{BASE_TYPES})\>)\s*"

    def dumps(self, obj):
        obj = Serelizator.dumpss(obj)
        return self.check_value(obj)

    def dump(self, obj, file):
        with open(file, 'w') as filee:
            filee.write(self.dumps(obj))

    def load(self, file_name):
        with open(file_name, 'r') as file:
            return self.loads(file.read())

    def loads(self, obj):
        obj = self.get_elem(obj)
        return Serelizator.loadss(obj)

    def check_value(self, obj):

        if isinstance(obj, (int, float, bool, complex)):
            # print("SER INT", obj, type(obj).__name__, str(obj))
            return self._create_elem(type(obj).__name__, str(obj))

        if isinstance(obj, str):
            value = self._change_symbol(obj)
            return self._create_elem("str", value)

        if isinstance(obj, list):
            value = "".join([self.check_value(v) for v in obj])
            return self._create_elem("list", value)

        if isinstance(obj, dict):
            value = "".join([f"{self.check_value(k)}\
                                       {self.check_value(v)}"\
                             for k, v in obj.items()])
            return self._create_elem("dict", value)

        if not obj:
            return self._create_elem("NoneType", "None")

    def get_elem(self, string):
        string = str(string)
        string = string.strip()

        match = regex.fullmatch(self.FIND_FOR_XML, string)

        if not match:
            return

        key = match.group("key")
        value = match.group("value")

        if key == "int":
            return int(value)

        if key == "float":
            return float(value)

        if key == "str":
            return self._change_symbol(value, True)

        if key == "bool":
            return value == "True"

        if key == "complex":
            return complex(value)

        if key == "NoneType":
            return None

        if key == "list":
            matches = regex.findall(self.FIND_FOR_XML, value)
            return [self.get_elem(match[0]) for match in matches]

        if key == "dict":
            matches = regex.findall(self.FIND_FOR_XML, value)
            return {self.get_elem(matches[i][0]):
                        self.get_elem(matches[i + 1][0]) \
                    for i in range(0, len(matches), 2)}

    def _create_elem(self, name, val):
        return f'<{name}>{val}</{name}>'

    def _change_symbol(self, string, reverse=False): #special xml symbols for xml doc
        if reverse:
            return string.replace("&amp;", "&").replace("&lt;", "<"). \
                replace("&gt;", ">").replace("&quot;", '"').replace("&apos;", "'")
        else:
            return string.replace("&", "&amp;").replace("<", "&lt;"). \
                replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")

