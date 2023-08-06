from dataclasses import dataclass
from typing import Any, Dict

from smartparams import Smart


@dataclass
class Params:
    param: str


def function_a(smart: Smart[Params]) -> str:
    return smart().param + 'function_a!'


def function_b(param: str) -> str:
    return param + 'function_b!'


def function_c(params: Smart[Dict[str, Any]]) -> str:
    return params()['param'] + 'function_c!'
