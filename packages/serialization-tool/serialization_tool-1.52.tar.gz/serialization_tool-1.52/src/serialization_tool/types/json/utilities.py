from .constants import VALUE, TYPE, ARRAY_IN_ARRAY_REGEX, ARRAY_REGEX, VALUE_REGEX, TYPES
from .constants import RegularExpressions as Expression
import regex



def to_json(obj) -> str:
    # if type(obj) == tuple:
    #     serialized = []
    #     for i in obj:
    #         serialized.append(f"{to_json(i)}")
    #     ans = ", ".join(serialized)
    #     return f"[{ans}]"
    # else:
    #     return f"\"{str(obj)}\""

    if isinstance(obj, TYPES):
        if isinstance(obj, str):
            return '"' + obj.replace("\\", "\\\\").replace('"', "\"").replace("'", "\'") + '"'
        else:
            return str(obj)

    if isinstance(obj, list):
        return '[' + ', '.join([to_json(item) for item in obj]) + ']'

    if isinstance(obj, dict):
        return '{' + ', '.join([f'{to_json(key)}: {to_json(value)}'
                                    for key, value in obj.items()]) + '}'

def from_json(string: str):
    string = string.strip()

    if regex.fullmatch(Expression.INT.value, string):
        return int(string)

    if regex.fullmatch(Expression.STR.value, string):
        string = string.replace("\\\\", "\\").replace(r"\"", '"').replace(r"\'", "'")
        return string[1:-1]

    if regex.fullmatch(Expression.FLOAT.value, string):
        return float(string)

    if regex.fullmatch(Expression.BOOL.value, string):
        return True if string == 'True' else False

    if regex.fullmatch(Expression.NONE.value, string):
        return None

    if string.startswith("[") and string.endswith("]"):
        string = string[1:-1]
        matches = regex.findall(Expression.ANY_VALUE.value, string)
        return [from_json(match[0]) for match in matches]

    if string.startswith("{") and string.endswith("}"):
        string = string[1:-1]
        matches = regex.findall(Expression.ANY_VALUE.value, string)
        return {from_json(matches[i][0]): from_json(matches[i + 1][0])
                    for i in range(0, len(matches), 2)}