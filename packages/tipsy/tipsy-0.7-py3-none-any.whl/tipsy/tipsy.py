import inspect
from collections.abc import Callable, Iterable, Mapping, MutableMapping, MutableSequence, MutableSet, Sequence, Set
from enum import Enum
from types import UnionType
from typing import Any, Literal, TypeGuard, TypeVar, get_args, get_origin, is_typeddict

from .cached import cached
from .registry import user_generic, user_types
from .types import TypeGuardFnc

T = TypeVar("T")


def cast_to_type(data: Any, t: type[T], strict: bool = False) -> T:
    if is_type(data, t, strict):
        return data
    else:
        raise TypeError(f"{data} is not of type {t}")


def is_type(data: Any, t: type[T], strict: bool = False) -> TypeGuard[T]:
    return guard(t, invariant=False, strict=strict)(data)


def is_mutable_collection(t: type[T]) -> bool:
    if issubclass(t, Mapping):
        return issubclass(t, MutableMapping)
    elif issubclass(t, Sequence):
        return issubclass(t, MutableSequence)
    elif issubclass(t, Set):
        return issubclass(t, MutableSet)
    else:
        return False


def get_super_type(t: type) -> type | None:
    return getattr(t, "__supertype__", None)


def _arg_hash(t: type[T], invariant: bool, strict: bool) -> int:
    return hash((t, invariant, strict))


@cached(_arg_hash)
def guard(t: type[T], invariant: bool, strict: bool) -> TypeGuardFnc[Any, T]:
    origin = get_origin(t)
    supertype = get_super_type(t)

    if t in user_types.keys():
        return user_types[t](t, invariant, strict)

    elif origin and origin in user_generic.keys():
        return user_generic[origin](t, invariant, strict)

    elif is_typeddict(t):
        gg = guard(dict, invariant, strict)
        invariant = is_mutable_collection(dict)
        kg = guard(str, False, strict)
        vgs = {k: guard(v, False, strict) for k, v in t.__annotations__.items()}
        required = t.__required_keys__  # type: ignore[attr-defined]
        optional = t.__optional_keys__  # type: ignore[attr-defined]

        def inner(data: Any) -> TypeGuard[T]:
            return (
                gg(data)
                and required <= set(data.keys())
                and set(data.keys()) <= required | optional
                and all(kg(x) for x in data.keys())
                and all(vgs[x](data[x]) for x in data.keys())
            )

    elif origin is tuple:
        gg = guard(origin, invariant, strict)
        vgs2 = [guard(x, invariant, strict) for x in get_args(t)]

        def inner(data: Any) -> TypeGuard[T]:
            return gg(data) and len(data) == len(vgs2) and all(vg(x) for vg, x in zip(vgs2, data))

    elif origin is Literal:
        literals = set(get_args(t))

        def inner(data: Any) -> TypeGuard[T]:
            return data in literals

    elif origin is Callable:
        gg = guard(origin, invariant, strict)
        at, rt = get_args(t)

        def inner(data: Any) -> TypeGuard[T]:
            sig = inspect.signature(data)
            params = [x.annotation for x in sig.parameters.values()]
            ret = sig.return_annotation
            return gg(data) and len(at) == len(params) and all(x is t for t, x in zip(at, params)) and ret is rt

    elif origin and issubclass(origin, Mapping):
        gg = guard(origin, invariant, strict)
        invariant = is_mutable_collection(origin)
        kg, vg = (guard(x, invariant, strict) for x in get_args(t))

        def inner(data: Any) -> TypeGuard[T]:
            return gg(data) and all(kg(x) for x in data.keys()) and all(vg(x) for x in data.values())

    elif origin and issubclass(origin, Iterable):
        gg = guard(origin, invariant, strict)
        invariant = is_mutable_collection(origin)
        vt = get_args(t)[0]
        vg = guard(vt, invariant, strict)

        def inner(data: Any) -> TypeGuard[T]:
            return gg(data) and all(vg(x) for x in data)

    elif origin is type:
        gg = guard(origin, invariant, strict)
        vt = get_args(t)[0]

        def inner(data: Any) -> TypeGuard[T]:
            return gg(data) and data is vt

    elif origin is UnionType:
        vgs2 = [guard(x, invariant, strict) for x in get_args(t)]

        def inner(data: Any) -> TypeGuard[T]:
            return False if (strict and invariant) else any(v(data) for v in vgs2)

    elif supertype:
        gg = guard(supertype, invariant, strict)

        def inner(data: Any) -> TypeGuard[T]:
            return False if strict else gg(data)

    elif t is Any:

        def inner(data: Any) -> TypeGuard[T]:
            return not (strict and invariant)

    elif issubclass(t, Enum):
        vgs3 = [x.value for x in t]

        def inner(data: Any) -> TypeGuard[T]:
            return data in vgs3

    else:

        def inner(data: Any) -> TypeGuard[T]:
            return type(data) is t if (strict and invariant) else isinstance(data, t)

    return inner
