from collections.abc import Callable
from functools import wraps
from typing import Concatenate, ParamSpec, TypeVar

P = ParamSpec("P")
T1 = TypeVar("T1")
T2 = TypeVar("T2")
R = TypeVar("R")


def curry1(fnc: Callable[Concatenate[T1, P], R]) -> Callable[[T1], Callable[P, R]]:
    @wraps(fnc)
    def outer(arg1: T1) -> Callable[P, R]:
        def innner(*args: P.args, **kwargs: P.kwargs) -> R:
            return fnc(arg1, *args, **kwargs)

        return innner

    return outer


def curry2(fnc: Callable[Concatenate[T1, T2, P], R]) -> Callable[[T1, T2], Callable[P, R]]:
    @wraps(fnc)
    def outer(arg1: T1, arg2: T2) -> Callable[P, R]:
        def innner(*args: P.args, **kwargs: P.kwargs) -> R:
            return fnc(arg1, arg2, *args, **kwargs)

        return innner

    return outer
