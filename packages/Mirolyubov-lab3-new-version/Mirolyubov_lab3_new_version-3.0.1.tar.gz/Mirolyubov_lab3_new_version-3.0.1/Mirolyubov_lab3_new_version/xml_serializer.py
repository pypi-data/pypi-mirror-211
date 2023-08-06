from Mirolyubov_lab3_new_version.packing import convert, deconvert
from Mirolyubov_lab3_new_version.CONSTANTS import PRIMITIVE_TYPES


class Xml:
    def __init__(self):
        self._dict_counter = 0
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

    def _serialize_dict(self, obj):
        result = f'<"{type(obj).__name__}">\n'
        self._indent += 4

        for key, value in obj.items():
            result += ' ' * self._indent + f'<{self._serialize_to_str(key)}>\n'
            self._indent += 4
            result += ' ' * self._indent + f'{self._serialize_to_str(value)}' + '\n'
            self._indent -= 4
            result += ' ' * self._indent + f'</{type(key).__name__}>' + '\n'

        if len(result) > 1 and result[-3] == ',':
            result = result[:-3]

        self._indent -= 4
        result += ' ' * self._indent + f'</"{type(obj).__name__}">'

        return result

    def _serialize_primitive(self, obj):
        result = ''

        if obj is None:
            result += f'<"{type(obj).__name__}">' + 'null' + f'</"{type(obj).__name__}">'

        elif isinstance(obj, bool):
            result += f'<"{type(obj).__name__}">' + 'true' + f'</"{type(obj).__name__}">' if obj\
                else f'<"{type(obj).__name__}">' + 'false' + f'</"{type(obj).__name__}">'

        elif isinstance(obj, (int, float)):
            result += f'<"{type(obj).__name__}">' + str(obj) + f'</"{type(obj).__name__}">'

        elif isinstance(obj, str):
            result += f'<"{type(obj).__name__}">' + f'{obj}' + f'</"{type(obj).__name__}">'

        return result

    def _serialize_collection(self, obj):
        result = f'<"{type(obj).__name__}">\n'
        self._indent += 4

        for i in obj:
                result += ' ' * self._indent + f'{self._serialize_to_str(i)}\n'

        self._indent -= 4
        result += ' ' * self._indent + f'</"{type(obj).__name__}">'

        return result

    def loads(self, s):
        self._current_position = 0
        return deconvert(self._deserialize_from_str(s))

    def load(self, file):
        return self.loads(file.read())

    def _deserialize_from_str(self, string):
        self._current_position = string.find('<"', self._current_position)

        if self._current_position != -1:
            self._current_position += len('<')  # add "type" length

        if self._current_position >= len(string) or self._current_position == -1:
            return None

        if string[self._current_position:self._current_position + len('"int"')] == '"int"':
            self._current_position += len('"int"')

            return self._deserialize_num(string)

        if string[self._current_position:self._current_position + len('"float"')] == '"float"':
            self._current_position += len('"float"')

            return self._deserialize_num(string)

        if string[self._current_position:self._current_position + len('"bool"')] == '"bool"':
            self._current_position += len('"bool"')

            return self._deserialize_bool(string)

        if string[self._current_position:self._current_position + len('"NoneType"')] == '"NoneType"':
            self._current_position += len('"NoneType"')

            return self._deserialize_null(string)

        if string[self._current_position:self._current_position + len('"str"')] == '"str"':
            self._current_position += len('"str"')

            return self._deserialize_str(string)

        if string[self._current_position:self._current_position + len('"dict"')] == '"dict"':
            self._dict_counter += 1
            self._current_position += len('"dict"')

            return self._deserialize_dict(string)

        if string[self._current_position:self._current_position + len('"list"')] == '"list"' or \
                string[self._current_position:self._current_position + len('"tuple"')] == '"tuple"' or \
                string[self._current_position:self._current_position + len('"set"')] == '"set"':

            self._current_position += 1
            ind_end = string.find('"', self._current_position)
            s_type = string[self._current_position: ind_end]
            self._current_position = ind_end + 2

            return self._deserialize_collection(string, s_type)

    def _deserialize_num(self, s):
        self._current_position = s.find('>', self._current_position) + len('>')
        s_pos = self._current_position

        while self._current_position < len(s) and\
                ((s[self._current_position].isdigit() or s[self._current_position] == '.') and s[self._current_position] != '<'):
            self._current_position += 1

        num = s[s_pos:self._current_position]
        self._current_position = s.find('>', self._current_position) + 1

        return float(num) if '.' in str(num) else int(num)

    def _deserialize_collection(self, s, s_type):
        res = []
        self._current_position = s.find('<', self._current_position + 1)
        while self._current_position < len(s) and\
                s[self._current_position: self._current_position + len(s_type) + 5] != f'</"{s_type}">':

            v = self._deserialize_from_str(s)
            res.append(v)
            self._current_position = s.find('<', self._current_position)

        if s_type == 'tuple':
            self._current_position += 1
            return tuple(res)

        elif s_type == 'set':
            self._current_position += 1
            return set(res)
        else:
            self._current_position += 1
            return res

    def _deserialize_dict(self, s):
        res = {}

        while self._current_position < len(s) and s[self._current_position:self._current_position+9] != '</"dict">':
            self._current_position = s.find('<', self._current_position)

            while s[self._current_position+1] == '/' and s[self._current_position:self._current_position+9] != '</"dict">':
                self._current_position = s.find('<', self._current_position+1)
            if s[self._current_position+1] == '/' and s[self._current_position:self._current_position+9] == '</"dict">':
                self._current_position = s.find('<', self._current_position + 1)
                return res
            k = self._deserialize_from_str(s)
            v = self._deserialize_from_str(s)

            res[k] = v

            if self._current_position == -1:
                return res
        return res

    def _deserialize_str(self, s):
        res = ''
        self._current_position = s.find('>', self._current_position) + 1

        while self._current_position < len(s) and s[self._current_position] != '<':
            res += s[self._current_position]
            self._current_position += 1

        self._current_position = s.find('>', self._current_position)
        return res

    def _deserialize_bool(self, s):
        self._current_position = s.find('>', self._current_position) + len('>')

        if s[self._current_position:self._current_position + 4] == "true":
            self._current_position = s.find('>', self._current_position) + 1
            return True

        else:
            self._current_position = s.find('>', self._current_position) + 1
            return False

    def _deserialize_null(self, s):
        self._current_position = s.find('>', self._current_position) + len('>')
        self._current_position = s.find('>', self._current_position) + 1

        return None