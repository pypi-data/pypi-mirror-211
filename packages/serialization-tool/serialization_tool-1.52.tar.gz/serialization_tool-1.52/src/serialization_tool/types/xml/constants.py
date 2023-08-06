import enum
from types import NoneType

KEY = 'KEY'
VALUE = 'VALUE'

VALUE_REGEX = r"<\w+>(.*)<\w+\/>"

TYPES = (int, float, bool, str, NoneType, complex)

class XmlRegularExpression(enum.Enum):
    TYPES = "|".join(map(lambda x: x.__name__, list(TYPES) + [list, dict]))
    ITEM = fr"\s*(\<(?P<{KEY}>{TYPES})\>(?P<{VALUE}>([^<>]*)|(?R)+)\</({TYPES})\>)\s*"
