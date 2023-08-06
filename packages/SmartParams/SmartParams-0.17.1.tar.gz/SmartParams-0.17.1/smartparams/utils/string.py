import json
from typing import Any, Optional, Tuple

from smartparams.exceptions import ArgumentParserError

KEY_SEPARATOR = '.'
OBJECT_SEPARATOR = ':'
PARAM_SEPARATOR = '='


def join_keys(*args: Optional[str]) -> str:
    return KEY_SEPARATOR.join(a for a in args if a is not None)


def join_objects(*args: Optional[str]) -> str:
    return OBJECT_SEPARATOR.join(a for a in args if a is not None)


def parse_param(param: str) -> Tuple[str, Any]:
    key, separator, raw_value = param.partition(PARAM_SEPARATOR)

    if not separator:
        raise ArgumentParserError(param)

    try:
        value = json.loads(raw_value)
    except json.decoder.JSONDecodeError:
        value = raw_value

    return key, value


def to_bool(value: str) -> bool:
    value = value.lower()
    if value in ('1', 'y', 'yes', 't', 'true'):
        return True

    if value in ('0', 'n', 'no', 'f', 'false'):
        return False

    raise ValueError(f"String value '{value}' is not like to boolean.")
