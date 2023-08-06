import enum
from types import NoneType
TYPE = "TYPE"
VALUE = "VALUE"

ARRAY_IN_ARRAY_REGEX = "\"VALUE\": \[\["
ARRAY_REGEX = "\"VALUE\": \["
VALUE_REGEX = "\"VALUE\": \{"

TYPES = (int, float, bool, str, NoneType, complex)


class RegularExpressions(enum.Enum):
    INT = r"[+-]?\d+"
    FLOAT = fr"({INT}(?:\.\d+)?(?:e{INT})?)"
    BOOL = r"((True)|(False))\b"
    STR = r"\"((\\\")|[^\"])*\""
    NONE = r"\b(None)\b"
    COMPLEX = fr"{FLOAT}{FLOAT}j"

    LIST_RECURSION = r"\[(?R)?(,(?R))*\]"
    DICT_RECURSION = r"\{((?R):(?R))?(?:,(?R):(?R))*\}"

    ANY_VALUE = fr"\s*({LIST_RECURSION}|" \
                fr"{DICT_RECURSION}|" \
                fr"{STR}|" \
                fr"{FLOAT}|" \
                fr"{BOOL}|" \
                fr"{INT}|" \
                fr"{NONE}|" \
                fr"{COMPLEX}\s*)"