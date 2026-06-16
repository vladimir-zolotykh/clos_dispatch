#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import types
from typing import Callable, MutableMapping, Any
import inspect
import time
from functools import wraps

Stamp = tuple[type, ...]


class MultiMethod:
    def __init__(self, name: str):
        self._name = name  # method name
        self.dir: dict[tuple[type, ...], Callable] = {}  # registered methods

    def register(self, func: Callable) -> None:
        sig = inspect.signature(func)
        stamp: tuple[type, ...] = tuple(
            parm.annotation for parm in sig.parameters.values()
        )[1:]
        self.dir[stamp] = func
        n = sum(parm.default is not inspect._empty for parm in sig.parameters.values())
        if 0 < n:
            self.dir[stamp[:-n]] = func

    def __get__(self, instance: object, owner: object = None) -> Callable:
        if instance is None:
            return self
        # return types.MethodType(self, self)
        return types.MethodType(self, instance)

    def __call__(self, *args, **kwds):
        stamp = tuple(type(a) for a in args[1:])
        try:
            return self.dir[stamp](*args, **kwds)
        except KeyError as exc:
            raise TypeError(f"No method for {stamp}") from exc


class MultiDict(dict):
    def __setitem__(self, key: str, val: Callable) -> None:
        if key in self:
            oval: Callable = self[key]
            if isinstance(oval, MultiMethod):
                mm: MultiMethod = oval
                mm.register(val)
            else:
                mm: MultiMethod = MultiMethod(key)
                mm.register(oval)
                mm.register(val)
            super().__setitem__(key, mm)
        else:
            super().__setitem__(key, val)


class MultiMeta(type):
    @classmethod
    def __prepare__(
        mcls, clsname: str, bases: tuple[type, ...], /, **kwds: Any
    ) -> MutableMapping[str, object]:
        return MultiDict()


def inscribed(func):
    sig = inspect.signature(func)
    types_ = "-".join(
        p.annotation.__name__ for k, p in sig.parameters.items() if k != "self"
    )

    @wraps(func)
    def wrapper(*args, **kwds):
        values = " ".join(str(a) for a in args[1:])
        print(f"{func.__name__}-{types_} {values}")
        res = func(*args, **kwds)
        return res

    return wrapper


class HasAdd(metaclass=MultiMeta):
    @inscribed
    def add(self, x: int, y: int) -> int:
        return x + y

    @inscribed
    def add(self, x: str, y: str) -> str:  # noqa: F811
        return f"{x}__{y}"

    @inscribed
    def add(self, x: float, y: float = 2.3) -> float:  # noqa: F811
        return x + y


class Date(metaclass=MultiMeta):
    """
    >>> d = Date(2012, 12, 21)
    >>> d.year, d.month, d.day
    (2012, 12, 21)
    >>> e = Date()
    >>> e.year, e.month, e.day
    (2026, 6, 16)
    """

    def __init__(self, year: int, month: int, day: int):
        self.year = year
        self.month = month
        self.day = day

    def __init__(self):  # noqa: F811
        t = time.localtime()
        self.__init__(t.tm_year, t.tm_mon, t.tm_mday)


class _TestHasAdd:
    """
    >>> ha = HasAdd()
    >>> ha.add(1, 2)
    add-int-int 1 2
    3
    >>> ha.add("a", "b")
    add-str-str a b
    'a__b'
    >>> ha.add(1.2, 3.4)
    add-float-float 1.2 3.4
    4.6
    >>> ha.add(1.2)
    add-float-float 1.2 2.3
    3.5
    >>> ha.add("a", 5)
    Traceback (most recent call last):
    ...
    TypeError: No method for (<class 'str'>, <class 'int'>)
    """


if __name__ == "__main__":
    ha = HasAdd()
    ha.add(1, 2)
    ha.add("a", "b")  # type: ignore
    ha.add(1.2, 3.4)  # type: ignore
    ha.add(1.2)  # type: ignore

# if __name__ == "__main__":
#     import doctest

#     doctest.testmod()
