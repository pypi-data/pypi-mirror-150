TYPE_PATTERN = r"^{type:(\w+),object:(.*)[]}]$"


CODE_OBJECT_ATTRIBUTES = [
    'co_argcount',
    'co_posonlyargcount',
    'co_kwonlyargcount',
    'co_nlocals',
    'co_stacksize',
    'co_flags',
    'co_code',
    'co_consts',
    'co_names',
    'co_varnames',
    'co_filename',
    'co_name',
    'co_firstlineno',
    'co_lnotab',
    'co_freevars',
    'co_cellvars'
]

ATTRIBUTES = "attributes"
GLOBALS = "globals"
CODE = "code"
SUPERCLASSES = "superclasses"
NAME = "name"
DOC = "doc"

MODULES = "modules"
MODULE = "module"

TYPE = "type"
VALUE = "value"
ARGUMENTS = "arguments"
INSTANCE = "instance"
CLASS = "class"
OBJECT = "object"

FUNCTION = "function"

DICT = "dict"
LIST = "list"
TUPLE = "tuple"

FLOAT = "float"
INT = "int"
NONE_TYPE = "none"
STRING = "str"
BOOL = "bool"

BYTES = "bytes"

TRUE = "true"
FALSE = "false"