import types

OBJECT_TYPE_REGEX = "'([\w\W]+)'"
REGEX_TYPE = r"\'(\w+)\'"

TYPE = "TYPE"
VALUE = "VALUE"
CLASS = "class"
OBJECT = "object"
DICTIONARY = "dict"
FUNCTION = "function"
BASE = "base"
DATA = "data"

NAME = "__name__"
BUILTINS = "__builtins__"
CLOSURE = "__closure__"
DOC = "__doc__"
GLOBALS = "__globals__"
OBJECT_NAME = "__object_type__"
FIELDS_NAME = "__fields__"
MODULE_NAME = "__module__name__"
ITERATOR = "iterator"


CODE = "__code__"
MODULE = "module"

TYPES = ["int", "float", "bool", "str", "complex", "NoneType"]
PRIMITIVES = (int, float, bool, str, types.NoneType, complex)

COLLECTIONS = (set, list, tuple, bytes, bytearray)


ITERABLE_TYPES = ["list", "tuple", "set", "bytes"]

METHOD_DECORATORS = (classmethod, staticmethod)

FUNCTION_ATTRIBUTES = [
    "__name__",
    "__globals__",
    "__closure__",
    "__defaults__",
    "__kwdefaults__",
    "__code__",
]

CLASS_ATTRIBUTE_NAMES = [
    "__class__",
    "__doc__",
    "__getattribute__",
    "__new__",
    "__setattr__",
]

NOT_SERIALIZING_CLASS_ATTRIBUTES = [
    "__name__",
    "__base__",
    "__basicsize__",
    "__dictoffset__",
    "__class__",
]

NOT_SERIALIZING_TYPES = (
    types.WrapperDescriptorType,
    types.MethodDescriptorType,
    types.BuiltinFunctionType,
    types.GetSetDescriptorType,
    types.MappingProxyType,
)

NOT_CLASS_ATTRIBUTES = [
    "__class__",
    "__getattribute__",
    "__new__",
    "__setattr__",
]

CODE_ATTRIBUTES = (
    "co_argcount",
    "co_posonlyargcount",
    "co_kwonlyargcount",
    "co_nlocals",
    "co_stacksize",
    "co_flags",
    "co_code",
    "co_consts",
    "co_names",
    "co_varnames",
    "co_filename",
    "co_name",
    "co_qualname",
    "co_firstlineno",
    "co_lnotab",
    "co_exceptiontable",
    "co_freevars",
    "co_cellvars",
)

CODE_OBJECT_ARGS = [
    "co_argcount",
    "co_posonlyargcount",
    "co_kwonlyargcount",
    "co_nlocals",
    "co_stacksize",
    "co_flags",
    "co_code",
    "co_consts",
    "co_names",
    "co_varnames",
    "co_filename",
    "co_name",
    "co_firstlineno",
    "co_lnotab",
    "co_freevars",
    "co_cellvars",
]
