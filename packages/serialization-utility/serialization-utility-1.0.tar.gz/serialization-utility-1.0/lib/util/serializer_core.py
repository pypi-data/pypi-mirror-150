import inspect
import types

from lib.constants import constants


def resolve_type(item):
    if isinstance(item, types.NoneType):
        return constants.NONE_TYPE
    elif isinstance(item, bool):
        return constants.BOOL
    elif isinstance(item, int):
        return constants.INT
    elif isinstance(item, float):
        return constants.FLOAT
    elif isinstance(item, str):
        return constants.STRING
    elif isinstance(item, bytes):
        return constants.BYTES
    elif isinstance(item, list):
        return constants.LIST
    elif isinstance(item, dict):
        return constants.DICT
    elif isinstance(item, tuple):
        return constants.TUPLE
    elif isinstance(item, types.FunctionType):
        return constants.FUNCTION


def serialize_primitive(item) -> dict[str: any]:
    return {
        constants.TYPE: resolve_type(item),
        constants.OBJECT: item
    }


def serialize_str(item: str) -> dict[str: any]:
    return {
        constants.TYPE: constants.STRING,
        constants.OBJECT: item.replace('\n', '')
    }


def serialize_bytes(item: bytes) -> dict[str: any]:
    return {
        constants.TYPE: constants.BYTES,
        constants.OBJECT: item.hex()
    }


def serialize_list_tuple(item) -> dict[str: any]:
    return {
        constants.TYPE: resolve_type(item),
        constants.OBJECT: [serialize(element) for element in item]
    }


def serialize_dict(item: dict) -> dict[str: any]:
    serialized_dict = {}
    for key, value in item.items():
        if key != '__annotations__':
            serialized_dict[key] = serialize(value)

    return {
        constants.TYPE: constants.DICT,
        constants.OBJECT: serialized_dict
    }


def serialize_code(item):
    elements = {}

    attributes = constants.CODE_OBJECT_ATTRIBUTES

    for attr in attributes:
        elements[attr] = serialize(item.__getattribute__(attr))

    return {
        constants.TYPE: constants.DICT,
        constants.OBJECT: elements
    }


def serialize_func(item) -> dict[str, any]:
    code = item.__code__

    names = code.__getattribute__("co_names")
    glob = item.__getattribute__("__globals__")

    globals = {}
    modules = []
    for name in names:
        if name == item.__name__:
            globals[name] = item.__name__
        elif name in glob and name not in __builtins__:
            if inspect.ismodule(glob[name]):
                modules.append(name)
            else:
                globals[name] = glob[name]

    return {
        constants.TYPE: constants.FUNCTION,
        constants.OBJECT: {
            constants.CODE: serialize(code),
            constants.GLOBALS: serialize(globals),
            constants.MODULES: serialize(modules)
        }
    }


def serialize_class(obj):
    obj_dict = dict(obj.__dict__)
    bases = list(obj.__bases__)

    for base in bases:
        if base.__name__ == 'object':
            bases.pop(bases.index(base))

    return {
        constants.TYPE: constants.CLASS,
        constants.OBJECT: {
            constants.NAME: serialize(obj.__name__),
            constants.SUPERCLASSES: serialize(tuple(bases)),
            constants.ATTRIBUTES: serialize_dict(obj_dict)
        }
    }


def serialize_instance(obj):
    return {
        constants.TYPE: constants.INSTANCE,
        constants.OBJECT: {
            constants.ARGUMENTS: serialize(obj.__dict__),
            constants.CLASS: serialize(obj.__class__)
        }
    }


def serialize(item):
    if inspect.ismethoddescriptor(item) or inspect.isbuiltin(item) \
            or inspect.isgetsetdescriptor(item) or inspect.ismemberdescriptor(item):
        return serialize(None)
    if isinstance(item, (types.NoneType, int, float, bool)):
        return serialize_primitive(item)
    if isinstance(item, str):
        return serialize_str(item)
    if isinstance(item, bytes):
        return serialize_bytes(item)
    if isinstance(item, (list, tuple)):
        return serialize_list_tuple(item)
    if isinstance(item, dict):
        return serialize_dict(item)
    if inspect.isfunction(item):
        return serialize_func(item)
    if isinstance(item, types.CodeType):
        return serialize_code(item)
    if inspect.isclass(item):
        return serialize_class(item)
    if isinstance(item, object):
        return serialize_instance(item)

    return serialize(None)


def deserialize_primitive(item):
    return item[constants.OBJECT]


def deserialize_none(item):
    return None


def deserialize_list(item):
    return [deserialize(item) for item in item[constants.OBJECT]]


def deserialize_tuple(item):
    return tuple(deserialize(item) for item in item[constants.OBJECT])


def deserialize_bytes(item):
    return bytes.fromhex(item[constants.OBJECT])


def deserialize_dict(item: dict):
    deserialized_dict = {}

    for key, value in item.items():
        deserialized_dict[key] = deserialize(value)

    return deserialized_dict


def deserialize_function(item: dict[str, any]) -> types.FunctionType:
    obj_dict = item[constants.OBJECT]

    code = deserialize(obj_dict[constants.CODE])
    globals_dict = deserialize(obj_dict[constants.GLOBALS])
    modules = deserialize(obj_dict[constants.MODULES])

    for module_name in modules:
        module = __import__(module_name)
        globals_dict[module_name] = module

    code_obj_attributes = constants.CODE_OBJECT_ATTRIBUTES
    code_args = []

    for attr in code_obj_attributes:
        code_args.append(code[attr])

    return types.FunctionType(types.CodeType(*code_args), globals_dict)


def deserialize_class(item: dict[str, any]) -> type:
    obj_dict = item[constants.OBJECT]

    name = deserialize(obj_dict[constants.NAME])
    attributes = deserialize(obj_dict[constants.ATTRIBUTES])
    superclasses: tuple = deserialize(obj_dict[constants.SUPERCLASSES])

    superclasses += object,

    return type(name, superclasses, attributes)


def deserialize_instance(item: dict[str, any]) -> object:
    obj_dict = item[constants.OBJECT]

    attributes = list(deserialize(obj_dict[constants.ARGUMENTS]).values())
    class_type = deserialize(obj_dict[constants.CLASS])

    return class_type(*attributes)


def deserialize(item: dict[str, any]):
    if item[constants.TYPE] in [constants.INT,
                                constants.FLOAT,
                                constants.BOOL,
                                constants.STRING]:
        return deserialize_primitive(item)
    if item[constants.TYPE] == constants.NONE_TYPE:
        return deserialize_none(item)
    if item[constants.TYPE] == constants.BYTES:
        return deserialize_bytes(item)
    if item[constants.TYPE] in [constants.LIST,
                                constants.MODULES]:
        return deserialize_list(item)
    if item[constants.TYPE] == constants.TUPLE:
        return deserialize_tuple(item)
    if item[constants.TYPE] == constants.DICT:
        return deserialize_dict(item[constants.OBJECT])
    if item[constants.TYPE] == constants.FUNCTION:
        return deserialize_function(item)
    if item[constants.TYPE] == constants.CLASS:
        return deserialize_class(item)
    if item[constants.TYPE] == constants.INSTANCE:
        return deserialize_instance(item)
