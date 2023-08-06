import re
from .constants import VALUE_REGEX, TYPES, KEY, VALUE
from types import NoneType
import regex
from .constants import XmlRegularExpression as Expression
import builtins

intent = 0


def to_xml(obj):
    if isinstance(obj, TYPES):
        if isinstance(obj, str):
            return create_xml_item(type(obj).__name__, to_special_xml(obj))
        else:
            return create_xml_item(type(obj).__name__, str(obj))

    if isinstance(obj, list):
        return create_xml_item(
            type(obj).__name__, "".join([to_xml(item) for item in obj])
        )

    if isinstance(obj, dict):
        return create_xml_item(
            type(obj).__name__,
            "".join([f"{to_xml(key)}{to_xml(value)}" for key, value in obj.items()]),
        )

def from_xml(string: str):
    string = string.strip()

    match = regex.fullmatch(Expression.ITEM.value, string)
    if not match:
        return

    key = match.group(KEY)
    value = match.group(VALUE)

    if key in map(lambda p: p.__name__, TYPES):
        if key == str.__name__:
            return from_special_xml(value)
        elif key == NoneType.__name__:
            return None
        elif key == bool.__name__:
            return True if value == 'True' else False
        else:
            return getattr(builtins, key)(value)

    if key == list.__name__:
        matches = regex.findall(Expression.ITEM.value, value)
        return [from_xml(match[0]) for match in matches]

    if key == dict.__name__:
        matches = regex.findall(Expression.ITEM.value, value)
        return {from_xml(matches[i][0]): from_xml(matches[i + 1][0])
                    for i in range(0, len(matches), 2)}

def create_xml_item(tag_name, value):
    return f"<{tag_name}>{value}</{tag_name}>"


def to_special_xml(string):
    return (
        string.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def from_special_xml(string):
    return (
        string.replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&apos;", "'")
    )
