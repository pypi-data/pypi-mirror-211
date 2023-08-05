from functools import wraps
from typing import Any, TypeVar

from toolz import curry

from .tipsy import guard
from .types import TypeGuard, TypeGuardFactory, TypeGuardFnc

P = TypeVar("P")
T = TypeVar("T")


@curry
def subtype(parent: type[P], fnc: TypeGuardFactory[P, T]) -> TypeGuardFactory[Any, T]:
    def outer(t: type[T], invariant: bool, strict: bool) -> TypeGuardFnc[Any, T]:
        pg = guard(parent, invariant, strict)
        fg = fnc(t, invariant, strict)

        def inner(data: Any) -> TypeGuard[T]:
            return pg(data) and fg(data)

        return inner

    return outer


def nongeneric(fnc: TypeGuardFnc[P, T]) -> TypeGuardFactory[P, T]:
    def outer(t: type[P], invariant: bool, strict: bool) -> TypeGuardFnc[P, T]:
        @wraps(fnc)
        def inner(data: P) -> TypeGuard[T]:
            return type(data) is t if strict and invariant else fnc(data)

        return inner

    return outer
