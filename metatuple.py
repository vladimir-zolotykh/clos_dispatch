#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import ClassVar
from operator import itemgetter


class TupleMeta(type):
    def __init__(cls, clsname, bases, clsdict):
        fields = clsdict.get("_fields", [])
        for n, name in enumerate(fields):
            setattr(cls, name, property(itemgetter(n)))


class MyTuple(tuple, metaclass=TupleMeta):
    _fields: ClassVar[list[str]]

    def __new__(cls, *args):
        if len(args) != (n := len(cls._fields)):
            raise TypeError(f"{cls} gets {n} args")
        return super().__new__(cls, args)


class Person(MyTuple):
    _fields = ["name", "age", "salary"]


def as_csv(tup: MyTuple) -> str:
    return ", ".join(f"{n}={getattr(tup, n)!r}" for n in tup._fields)


if __name__ == "__main__":
    bob = Person("Bob", 37, 12000)
    print(bob)
    print(as_csv(bob))
