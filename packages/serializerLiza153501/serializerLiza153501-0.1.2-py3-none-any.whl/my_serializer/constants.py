import types

BASE_TYPES = {"str": str, "int": int, "bool": bool, "float": float, "complex": complex}

BASE_COLLECTIONS = {"list": list, "tuple": tuple, "frozenset": frozenset, "set": set, "bytes": bytes,
                    "bytearray": bytearray, "dict": dict}

SIMILAR_COLLECTIONS = {"list": list, "tuple": tuple, "frozenset": frozenset, "set": set, "bytes": bytes,
                       "bytearray": bytearray}

CODE_ATTRIBUTES = ("co_argcount",
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
                    #"co_qualname",
                    "co_firstlineno",
                    "co_lnotab",
                    #"co_exceptiontable",
                    "co_freevars",
                    "co_cellvars")

CLASS_PROPERTIES = ("__name__", "__base__",
                          "__basicsize__", "__dictoffset__", "__class__")

TYPESES = (
                types.WrapperDescriptorType,
                types.MethodDescriptorType,
                types.BuiltinFunctionType,
                types.GetSetDescriptorType,
                types.MappingProxyType
            )

METHODS = {"staticmethod": staticmethod, "classmethod": classmethod}

#regex
INT_REGULAR = r"[+-]?\d+"
FLOAT_REGULAR = r"(?:[+-]?\d+(?:\.\d+)?(?:e[+-]?\d+)?)"
BOOL_REGULAR = r"((?:true)|(?:false))\b"
STR_REGULAR = r"\"(?:(?:\\\")|[^\"])*\""
NONE_REGULAR = r"\b(?:Null)\b"
COMPLEX_REGULAR = fr"{INT_REGULAR}{INT_REGULAR}j"

LIST_RECURSION = r"\[(?R)?(?:,(?R))*\]"
VALUE_RECURSION = r"\{(?:(?R):(?R))?(?:,(?R):(?R))*\}"

VALUE_REGULAR_EXPR = fr"\s*({LIST_RECURSION}|{VALUE_RECURSION}|{STR_REGULAR}|{FLOAT_REGULAR}|" \
                fr"{BOOL_REGULAR}|{INT_REGULAR}|{NONE_REGULAR}|{COMPLEX_REGULAR}\s*)"

BASES_TYPES = r"str|int|float|bool|NoneType|list|dict"
key = fr"key"
val = fr"value"

ELEMENT_REGULAR = fr"\s*(\<(?P<{key}>{BASES_TYPES})\>(?P<{val}>([^<>]*)|(?R)+)\</(?:{BASES_TYPES})\>)\s*"