from Mirolyubov_lab3_new_version.packing import convert, deconvert
from Mirolyubov_lab3_new_version.CONSTANTS import PRIMITIVE_TYPES


class Json:
    def __init__(self):
        self._current_position = 0
        self._indent = 0

    def dumps(self, obj):
        return self._serialize_to_str(convert(obj))

    def dump(self, obj, file):
        file.write(self.dumps(obj))

    def _serialize_to_str(self, object):
        if isinstance(object, PRIMITIVE_TYPES):
            return self._serialize_primitive(object)

        elif isinstance(object, (list, tuple, set)):
            return self._serialize_collection(object)

        elif isinstance(object, dict):
            return self._serialize_dict(object)

        else:
            raise Exception("Unknown type to serialize")

    def _serialize_collection(self, obj):
        result = '\n' + ' ' * self._indent + '{\n'
        result += ' ' * self._indent + f'"type": "{type(obj).__name__}"\n'
        result += ' ' * self._indent + '"value": ['

        self._indent += 4

        for i in obj:
            result += self._serialize_to_str(i) + ','

        if len(result) > 1 and result[-1] == ',':
            result = result[:-1]

        self._indent -= 4
        result += '\n' + ' ' * self._indent + ']\n' + ' ' * self._indent + '}'

        return result

    def _serialize_primitive(self, obj):
        result = '\n' + ' ' * self._indent + '{\n'
        result += ' ' * self._indent + f'"type": "{type(obj).__name__}"\n'
        result += ' ' * self._indent + '"value": '

        if obj is None:
            result += 'null'

        elif isinstance(obj, bool):
            result += 'true' if obj else 'false'

        elif isinstance(obj, (int, float)):
            result += str(obj)

        elif isinstance(obj, str):
            result += f'"{obj}"'

        result += '\n' + ' ' * self._indent + '}'

        return result

    def _serialize_dict(self, obj):
        result = '\n' + ' ' * self._indent + '{\n'
        result += ' ' * self._indent + f'"type": "{type(obj).__name__}"\n'
        result += ' ' * self._indent + '"value": {'

        self._indent += 4

        for key, value in obj.items():
            result += self._serialize_to_str(key) + ': ' + self._serialize_to_str(value) + ', \n'

        if len(result) > 1 and result[-3] == ',':
            result = result[:-3]

        result += '\n' + ' ' * self._indent + '}\n'
        self._indent -= 4
        result += ' ' * self._indent + '}'

        return result

    def loads(self, s):
        self._current_position = 0
        return deconvert(self._deserialize_from_str(s))

    def load(self, file):
        return self.loads(file.read())

    def _deserialize_from_str(self, string):
        self._current_position = string.find('"type":', self._current_position)

        if self._current_position != -1:
            self._current_position += len('"type": ')  # add "type" length

        if self._current_position >= len(string) or self._current_position == -1:
            return

        if string[self._current_position:self._current_position + len('"int"')] == '"int"':
            self._current_position += len('"int"\n')

            return self._deserialize_num(string)

        if string[self._current_position:self._current_position + len('"float"')] == '"float"':
            self._current_position += len('"float"\n')

            return self._deserialize_num(string)

        if string[self._current_position:self._current_position + len('"bool"')] == '"bool"':
            self._current_position += len('"bool"\n')

            return self._deserialize_bool(string)

        if string[self._current_position:self._current_position + len('"NoneType"')] == '"NoneType"':
            self._current_position += len('"NoneType"\n')

            return self._deserialize_null(string)

        if string[self._current_position:self._current_position + len('"str"')] == '"str"':
            self._current_position += len('"str"\n')

            return self._deserialize_str(string)

        if string[self._current_position:self._current_position + len('"dict"')] == '"dict"':
            self._current_position += len('"dict"\n')

            return self._deserialize_dict(string)

        if string[self._current_position:self._current_position + len('"list"')] == '"list"' or \
                string[self._current_position:self._current_position + len('"tuple"')] == '"tuple"' or \
                string[self._current_position:self._current_position + len('"set"')] == '"set"':

            self._current_position += 1
            ind_end = string.find('"', self._current_position)
            s_type = string[self._current_position: ind_end]
            self._current_position = ind_end + 1

            return self._deserialize_collection(string, s_type)

    def _deserialize_num(self, s):
        self._current_position = s.find('"value": ', self._current_position) + len('"value": ')
        s_pos = self._current_position

        while self._current_position < len(s) and\
                (s[self._current_position].isdigit() or s[self._current_position] == '.'):
            self._current_position += 1

        num = s[s_pos:self._current_position]
        self._current_position = s.find('}', self._current_position) + 1

        return float(num) if '.' in str(num) else int(num)

    def _deserialize_bool(self, s):
        self._current_position = s.find('"value": ', self._current_position) + len('"value": ')

        if s[self._current_position:self._current_position + 4] == "true":
            self._current_position = s.find('}', self._current_position) + 1

            return True

        else:
            self._current_position = s.find('}', self._current_position) + 1

            return False

    def _deserialize_null(self, s):
        self._current_position = s.find('"value": ', self._current_position) + len('"value": ')
        self._current_position = s.find('}', self._current_position) + 1

        return None

    def _deserialize_str(self, s):
        self._current_position = s.find('"value": ', self._current_position) + len('"value": ')

        res = ""
        self._current_position += 1

        while self._current_position < len(s) and s[self._current_position:self._current_position + 1] not in '"\n':
            res += s[self._current_position]
            self._current_position += 1

        self._current_position = s.find('}', self._current_position) + 1

        return res

    def _deserialize_dict(self, s):
        self._current_position = s.find('"value": ', self._current_position) + len('"value": ')
        res = {}

        self._current_position += 1

        while self._current_position < len(s) and s[self._current_position] != '}':
            if s[self._current_position] in (' ', ',', ':', '\n'):
                self._current_position += 1
                continue

            k = self._deserialize_from_str(s)
            v = self._deserialize_from_str(s)
            res[k] = v

        self._current_position = s.find('}', self._current_position + 1) + 1

        return res

    def _deserialize_collection(self, s, s_type):
        self._current_position = s.find('"value": ', self._current_position) + len('"value": ')

        res = []
        self._current_position += 1

        while self._current_position < len(s) and s[self._current_position] != ']':
            if s[self._current_position] in (' ', ',', '\n'):
                self._current_position += 1
                continue

            v = self._deserialize_from_str(s)
            res.append(v)

        self._current_position = s.find('}', self._current_position) + 1

        if s_type == 'tuple':
            return tuple(res)

        elif s_type == 'set':
            return set(res)

        return res