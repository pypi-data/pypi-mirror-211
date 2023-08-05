from typing import Any, TypeVar

from toolz import curry

from .types import TypeGuardFactory

P = TypeVar("P")
T = TypeVar("T")


class Registry(dict):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def __getitem__(self, __key: type[T]) -> TypeGuardFactory[Any, T]:
        return super().__getitem__(__key)

    def __setitem__(self, __key: type[T], __value: TypeGuardFactory[Any, T]) -> None:
        return super().__setitem__(__key, __value)


user_types = Registry()
user_generic = Registry()


@curry
def register_type(t: type[T], fnc: TypeGuardFactory[Any, T]) -> TypeGuardFactory[Any, T]:
    user_types[t] = fnc
    return fnc


@curry
def register_generic(t: type[T], fnc: TypeGuardFactory[Any, T]) -> TypeGuardFactory[Any, T]:
    user_generic[t] = fnc
    return fnc
