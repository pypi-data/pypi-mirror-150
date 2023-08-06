import os.path
from typing import Any, Dict, List, Optional, Tuple

import smartparams.utils.string as strutil


def flatten_keys(
    obj: Any,
    _prefix: Optional[str] = None,
) -> List[str]:
    if not obj or not isinstance(obj, dict) or not all(isinstance(key, str) for key in obj):
        return [] if _prefix is None else [_prefix]

    keys = []
    for k, v in obj.items():
        keys.extend(flatten_keys(v, strutil.join_keys(_prefix, k)))

    return keys


def find_nested(
    dictionary: Dict[str, Any],
    key: str,
    create_mode: bool = False,
    set_mode: bool = False,
    required: bool = False,
) -> Tuple[Dict[str, Any], str]:
    *nested_keys, last_key = key.split(strutil.KEY_SEPARATOR)

    key_list = list()
    for k in nested_keys:
        key_list.append(k)
        if k not in dictionary:
            if create_mode:
                dictionary[k] = dict()
            elif not required:
                return dict(), last_key
            else:
                key_trace = strutil.KEY_SEPARATOR.join(key_list)
                raise KeyError(f"Subkey '{key_trace}' of '{key}' is not in dictionary.")

        if not isinstance(dictionary[k], dict):
            if set_mode:
                dictionary[k] = dict()
            else:
                key_trace = strutil.KEY_SEPARATOR.join(key_list)
                raise KeyError(f"Subkey '{key_trace}' of '{key}' is not dictionary.")

        dictionary = dictionary[k]

    if required and last_key not in dictionary:
        raise KeyError(f"Key '{key}' is not in dictionary.")

    return dictionary, last_key


def check_key_is_in(
    key: str,
    dictionary: Dict[str, Any],
) -> bool:
    key, separator, sub_key = key.partition(strutil.KEY_SEPARATOR)
    if key not in dictionary:
        return False

    if not separator:
        return True

    dictionary = dictionary[key]

    if not isinstance(dictionary, dict):
        return True

    return check_key_is_in(
        key=sub_key,
        dictionary=dictionary,
    )


def normalize(
    dictionary: Dict,
    trace: str = '',
) -> Dict:
    if not all(isinstance(key, str) for key in dictionary):
        return dictionary

    normalized_dictionary: Dict = {}
    for key, value in dictionary.items():
        key, separator, sub_key = key.partition(strutil.KEY_SEPARATOR)
        if separator:
            value = {sub_key: value}

        current_trace = strutil.join_keys(trace, key)

        if isinstance(value, dict):
            value = normalize(
                dictionary=value,
                trace=current_trace,
            )

        if key in normalized_dictionary:
            value = merge(
                a=normalized_dictionary[key],
                b=value,
                trace=current_trace,
            )

        normalized_dictionary[key] = value

    return normalized_dictionary


def merge(
    a: Any,
    b: Any,
    trace: str = '',
) -> Any:
    if isinstance(a, dict) and isinstance(b, dict):
        dictionary = {}
        intersection = set(a).intersection(b)
        for key in set(a).union(b):
            if key in intersection:
                if not isinstance(key, str):
                    raise KeyError(f"Cannot merge dictionaries with non-string keys: '{trace}'.")

                dictionary[key] = merge(
                    a=a[key],
                    b=b[key],
                    trace=strutil.join_keys(trace, key),
                )
            else:
                dictionary[key] = a.get(key, b.get(key))

        return dictionary

    raise ValueError(f"Cannot merge dictionaries with key: '{trace}'.")


def flatten_unique_keys(flatten_dictionary: Dict[str, Any]) -> Dict[str, Any]:
    keys = {key: key.split(strutil.KEY_SEPARATOR)[::-1] for key in flatten_dictionary}

    for key, value in keys.items():
        index = max(len(os.path.commonprefix((value, v))) for k, v in keys.items() if key != k)
        keys[key] = value[: index + 1]

    return {
        strutil.KEY_SEPARATOR.join(keys[key][::-1]): value
        for key, value in flatten_dictionary.items()
    }
