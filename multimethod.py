#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
import types
from typing import Callable
import inspect


class MultiMethod:
    def __init__(self, name: str):
        self._name = name  # method name
        self.dir: dict[str, MultiMethod] = {}  # registered methods

    def register(self, func: Callable):
        sig = inspect.signature(func)
        stamp: tuple[type, ...] = tuple(
            parm.annotation for parm in sig.parameters.values()
        )[1:]
        self.dir[stamp] = func
        n = sum(parm.default is inspect._empty for parm in sig.parameters.values())
        if 0 < n:
            self.dir[stamp[:-n]] = func

    def __get__(self, instance, owner=None) -> Callable:
        if instance is None:
            return self
        # return types.MethodType(self, self)
        return types.MethodType(self, instance)

    def __call__(self, *args, **kwds):
        stamp = tuple(type(a) for a in args[1:])
        return self.dir[stamp](*args, **kwds)


class MultiDict(dict):
    def __setitem__(self, key: str, val: Callable):
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
    def __prepare__(cls, clsname, bases, clsdict):
        return MultiDict()


class HasAdd(metaclass=MultiMeta):
    def add(x: int, y: int):
        print(f"add-int-int {x} {y}")
        return x + y

    def add(x: str, y: str):  # noqa: F811
        print(f"add-str-str {x} {y}")
        return f"{x}__{y}"

    def add(x: float, y: float = 2.3):  # noqa: F811
        print(f"add-float-float {x} {y}")
        return x + y


if __name__ == "__main__":
    ha = HasAdd()
    ha.add(1, 2)
    ha.add("a", "b")
    ha.add(1.2, 3.4)
    ha.add(1.2)
