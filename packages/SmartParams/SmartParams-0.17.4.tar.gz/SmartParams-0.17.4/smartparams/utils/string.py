import json
from pathlib import Path
from typing import Any, List, Optional, Tuple

from smartparams.exceptions import ArgumentParserError

KEY_SEPARATOR = '.'
OBJECT_SEPARATOR = ':'
PARAM_SEPARATOR = '='
MODE_SEPARATOR = ','
PATH_SEPARATOR = '/'
OPTIONAL_SUFFIX = '?'


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


def parse_mode(
    path: Path,
    mode: str,
) -> List[Tuple[Path, bool]]:
    modes = []
    for mode in mode.split(MODE_SEPARATOR):
        *sub_dir, mode = mode.split(PATH_SEPARATOR)

        if mode.endswith(OPTIONAL_SUFFIX):
            required = False
            mode = mode[:-1]
        else:
            required = True

        suffix = f'.{mode}{path.suffix}'
        modes.append((path.parent.joinpath(*sub_dir, path.stem).with_suffix(suffix), required))

    return modes
