from typing import Any, Dict, List, Set, Tuple, Type

from smartparams.smart import Smart

CONSTANT = 'constant'


class Class:
    def __init__(self, arg1: str, arg2: int = 5) -> None:
        self.arg1 = arg1
        self.arg2 = arg2


class ClassChild(Class):
    pass


class ClassComposition:
    def __init__(  # type: ignore
        self,
        vanilla_cls: Class,
        smart_cls: Smart[Class],
        smart: Smart,
        class_type: Type[Class],
        unknown: Any,
    ) -> None:
        self.vanilla_cls = vanilla_cls
        self.smart_cls = smart_cls
        self.smart = smart
        self.class_type = class_type
        self.unknown = unknown


class ClassCompositionChild(ClassComposition):
    def __init__(  # type: ignore
        self,
        vanilla_cls: Class,
        smart_cls: Smart[Class],
        smart: Smart,
        unknown: Any,
        no_type,
        *args: Any,
        with_only_default_primitive=11,
        **kwargs: Any,
    ) -> None:
        super(ClassCompositionChild, self).__init__(
            vanilla_cls=vanilla_cls,
            smart_cls=smart_cls,
            smart=smart,
            unknown=unknown,
            class_type=Class,
        )
        self.no_type = no_type
        self.args = args
        self.with_only_default_primitive = with_only_default_primitive
        self.kwargs = kwargs


class RaiseClass:
    def __init__(self) -> None:
        raise RuntimeError


class Iter:
    def __init__(  # type: ignore
        self,
        di: Dict,
        li: List,
        tu: Tuple,
        se: Set,
        tu_d=(0, 1),
    ) -> None:
        self.di = di
        self.li = li
        self.tu = tu
        self.se = se
        self.tu_d = tu_d


def some_function() -> None:
    pass
