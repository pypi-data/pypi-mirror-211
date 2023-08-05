import types

from core.formats.xml.constants import FIRST_XML_ELEMENT_PATTERN, XML_ELEMENT_PATTERN, KEY_GROUP_NAME, VALUE_GROUP_NAME, \
    XML_SCHEME_PATTERN
import regex


def parse_json(item):
    if item == "[]":
        return {}
    elif item[0] == "{" or item[0] == "[":
        is_list = item[0] == "["
        item = item[1:-1]
        result = {}
        result_list = []
        depth = 0
        in_quotes = False
        temp_str = ""
        key = ""
        value = ""

        for char in item:
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
            elif char == "[":
                depth += 1
            elif char == "]":
                depth -= 1
            elif char == "\"":
                in_quotes = not in_quotes
            elif char == ":" and not in_quotes and depth == 0:
                key += temp_str[1:-1]
                temp_str = ""
                continue
            elif char == "," and not in_quotes and depth == 0 and not is_list:
                value += temp_str[1:-1]
                result[key] = value
                value = ""
                key = ""
                temp_str = ""
                continue
            elif char == "," and is_list and depth == 0:
                result_list.append(parse_json(temp_str))
                temp_str = ""
                continue
            elif char == ' ' and not in_quotes:
                continue

            temp_str += char

        if temp_str[0] == "'" or temp_str[0] == '"':
            result[key] = temp_str[1:-1]
        elif is_list:
            result_list.append(parse_json(temp_str))
        else:
            result[key] = parse_json(temp_str)
    else:
        return item

    if is_list:

        return result_list
    else:
        return result



def dumps_from_dict(obj, is_first=False) -> str:
    if type(obj) in (int, float, bool, types.NoneType):
        return create_xml_element(type(obj).__name__, str(obj), is_first)
    elif type(obj) is str:
        data = mask_symbols(obj)
        return create_xml_element(str.__name__, data, is_first)
    elif type(obj) is list:
        data = ''.join([dumps_from_dict(o) for o in obj])
        return create_xml_element(list.__name__, data, is_first)
    elif type(obj) is dict:
        data = ''.join(
            [f"{dumps_from_dict(item[0])}{dumps_from_dict(item[1])}" for item in obj.items()])
        return create_xml_element(dict.__name__, data, is_first)


def loads_to_dict(string: str, is_first=False):
    string = string.strip()
    xml_element_pattern = FIRST_XML_ELEMENT_PATTERN if is_first else XML_ELEMENT_PATTERN

    match = regex.fullmatch(xml_element_pattern, string)

    if not match:
        raise ValueError

    key = match.group(KEY_GROUP_NAME)
    value = match.group(VALUE_GROUP_NAME)

    if key == int.__name__:
        return int(value)
    elif key == float.__name__:
        return float(value)
    elif key == bool.__name__:
        return value == str(True)
    elif key == str.__name__:
        return unmask_symbols(value)
    elif key == types.NoneType.__name__:
        return None
    elif key == list.__name__:
        matches = regex.findall(XML_ELEMENT_PATTERN, value)
        return [loads_to_dict(match[0]) for match in matches]
    elif key == dict.__name__:
        matches = regex.findall(XML_ELEMENT_PATTERN, value)
        return {loads_to_dict(matches[i][0]):
                    loads_to_dict(matches[i + 1][0]) for i in range(0, len(matches), 2)}


def create_xml_element(name: str, data: str, is_first=False):
    if is_first:
        return f"<{name} {XML_SCHEME_PATTERN}>{data}</{name}>"
    else:
        return f"<{name}>{data}</{name}>"


def mask_symbols(string: str) -> str:
    return string.replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;"). \
        replace('"', "&quot;").replace("'", "&apos;")


def unmask_symbols(string: str) -> str:
    return string.replace("&amp;", '&').replace("&lt;", '<').replace("&gt;", '>'). \
        replace("&quot;", '"').replace("&apos;", "'")
