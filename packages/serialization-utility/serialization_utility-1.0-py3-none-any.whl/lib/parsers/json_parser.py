import re

from lib.constants import constants
from lib.parsers.parser import Serializer
from lib.parsers.serializer_core import serialize, deserialize


class JsonSerializer(Serializer):
    @staticmethod
    def to_string(item):
        if isinstance(item, dict):
            strings = []

            for key, value in item.items():
                strings.append(f"{JsonSerializer.to_string(key)}:{JsonSerializer.to_string(value)},")

            return f"{{{''.join(strings)[:-1]}}}" \
                .replace('True', 'true') \
                .replace('False', 'false') \
                .replace('None', 'null') \
                .replace('\'', "\"")

        elif isinstance(item, str):
            string = item.translate(str.maketrans({
                "\"": r"\"",
                "\\": r"\\",
            }))

            return f"\"{string}\""

        elif item is None:
            return "null"
        elif item is True:
            return constants.TRUE
        elif item is False:
            return constants.FALSE
        else:
            return str(item)

    @staticmethod
    def extract_list_items(list_str: str):
        balance = 0
        items = []
        flag = False
        i = 0
        for j in range(len(list_str)):
            if list_str[j] == '{':
                if balance == 0:
                    i = j
                    flag = True
                balance += 1
            elif list_str[j] == '}':
                balance -= 1
            if flag and balance == 0:
                items.append(JsonSerializer.from_string(list_str[i:j + 1]))
                flag = False

        return items

    @staticmethod
    def extract_dict_items(dict_str: str):
        try:
            type, obj = JsonSerializer.get_typed_object_info(dict_str)

            return {
                constants.TYPE: type,
                constants.OBJECT: JsonSerializer.resolve_obj(obj, type)
            }
        except AttributeError:
            balance = 0
            items = {}
            i = 1
            key = None
            value: any
            for j in range(0, len(dict_str)):
                if not j == 0 and dict_str[j] == '{':
                    balance += 1
                elif not j == len(dict_str) - 1 and dict_str[j] == '}':
                    balance -= 1
                if balance == 0 and dict_str[j] == ':':
                    key = dict_str[i:j]
                    i = j + 1
                if key is not None and balance == 0 and (dict_str[j] == ',' or j == len(dict_str) - 1):
                    value = dict_str[i:j]
                    items[key] = JsonSerializer.extract_dict_items(value)
                    i = j + 1

            return items

    @staticmethod
    def resolve_obj(obj, type):
        if type == constants.INT:
            return int(obj)
        if type == constants.FLOAT:
            return float(obj)
        if type == constants.BOOL:
            if obj == constants.TRUE:
                return True
            else:
                return False
        if type == constants.STRING or type == constants.BYTES:
            return obj
        if type == constants.NONE_TYPE:
            return None
        if type in [constants.LIST,
                    constants.TUPLE]:
            return JsonSerializer.extract_list_items(obj)
        if type in [constants.DICT,
                    constants.FUNCTION,
                    constants.MODULE,
                    constants.CLASS,
                    constants.INSTANCE]:
            return JsonSerializer.extract_dict_items(obj)

    @staticmethod
    def get_typed_object_info(obj_str: str) -> tuple[str, str]:
        groups = re.search(constants.TYPE_PATTERN, obj_str)
        type = groups.group(1)
        obj = groups.group(2)

        return type, obj

    @staticmethod
    def from_string(json_string: str) -> dict[str, any]:
        try:
            type, obj = JsonSerializer.get_typed_object_info(json_string)

            return {
                constants.TYPE: type,
                constants.OBJECT: JsonSerializer.resolve_obj(obj, type)
            }
        except AttributeError as e:
            print(f"Error: {e.args[0]}")

    def dumps(self, item):
        return JsonSerializer.to_string(serialize(item))

    def loads(self, string):
        string = re.sub(r'[\s\"\']+', '', string)
        dict_from_json = JsonSerializer.from_string(string)
        return deserialize(dict_from_json)
