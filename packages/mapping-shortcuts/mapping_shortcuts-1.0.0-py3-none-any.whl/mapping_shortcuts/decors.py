
from typing import TypeVar, Callable

KT = TypeVar('KT')
VT = TypeVar('VT')
WrapType = Callable[[VT], VT]
DecoratorType = Callable[[KT], WrapType[VT]]
CollectionType = dict[KT, VT]


def create_collector(
    raise_on_duplicate: bool = True
) -> tuple[DecoratorType[KT, VT], CollectionType[KT, VT]]:
    def decor(key: KT) -> WrapType[VT]:
        def wrap(func: VT) -> VT:
            if key in collection and raise_on_duplicate:
                raise ValueError(f'Duplication for key {key}')
            collection[key] = func
            return func
        return wrap
    collection = {}  # type: CollectionType[KT, VT]
    return decor, collection
