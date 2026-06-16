#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
# flake8: noqa: F811
# mypy: disable-error-code="no-redef"
import types
from typing import Callable, MutableMapping, Any
import inspect

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


class HasAdd(metaclass=MultiMeta):
    def add(self, x: int, y: int) -> int:
        print(f"add-int-int {x} {y}")
        return x + y

    def add(self, x: str, y: str) -> str:
        print(f"add-str-str {x} {y}")
        return f"{x}__{y}"

    def add(self, x: float, y: float = 2.3) -> float:
        print(f"add-float-float {x} {y}")
        return x + y


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
    import doctest

    doctest.testmod()
