from PikhtovSerLib.my_serelizator import Serelizator
from PikhtovSerLib.constants import INT_P, FLOAT_P, BOOL_P, STR_P, \
    NONE_P, VALUE_P
import regex


class JsonSerelizator:
    def dumps(self, obj):
        obj = Serelizator.dumpss(obj)
        return self.check_value(obj)

    def dump(self, obj, file):
        with open(file, 'w+') as filee:
            filee.write(self.dumps(obj))

    def load(self, file_name):
        with open(file_name, 'r') as file:
            return self.loads(file.read())

    def loads(self, obj):
        obj = self.get_elem(obj)
        return Serelizator.loadss(obj)

    def check_value(self, value):
        if isinstance(value, str):
            return '"' + value.replace("\\", "\\\\"). \
                replace('"', "\""). \
                replace("'", "\'") + '"'

        elif isinstance(value, (int, float, complex)):
            return str(value)

        elif isinstance(value, bool):
            return "true" if value else "false"

        elif isinstance(value, list):
            return "[" + ", ".join([self.check_value(val) for val in value]) + "]"

        if isinstance(value, dict):
            return "{" + ", ".join([f"{self.check_value(k)}: \
                                            {self.check_value(v)}" for k, v in value.items()]) + "}"

    def get_elem(self, string):
        string = string.strip()

        match = regex.fullmatch(INT_P, string)
        if match:
            return int(match.group(0))

        match = regex.fullmatch(STR_P, string)
        if match:
            res = match.group(0)
            res = res.replace("\\\\", "\\"). \
                replace(r"\"", '"'). \
                replace(r"\'", "'")
            return res[1:-1]

        match = regex.fullmatch(FLOAT_P, string)
        if match:
            return float(match.group(0))

        match = regex.fullmatch(BOOL_P, string)
        if match:
            return match.group(0) == "true"

        match = regex.fullmatch(NONE_P, string)
        if match:
            return None

        if string.startswith("[") and string.endswith("]"):
            string = string[1:-1]
            matches = regex.findall(VALUE_P, string)
            return [self.get_elem(match[0]) for match in matches]

        if string.startswith("{") and string.endswith("}"):
            string = string[1:-1]
            matches = regex.findall(VALUE_P, string)

            return {self.get_elem(matches[i][0]):
                        self.get_elem(matches[i + 1][0])
                    for i in range(0, len(matches), 2)}
