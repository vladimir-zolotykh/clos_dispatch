#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from collections import defaultdict


class CachedMeta(type):
    _cache = defaultdict(defaultdict)

    def __call__(cls, *args, **kwds):
        key = tuple(args)
        if cls not in (ca := type(cls)._cache) or key not in ca[cls]:
            ca[cls][key] = super().__call__(*args, **kwds)
        return ca[cls][key]


class Person(metaclass=CachedMeta):
    def __init__(self, name, age, salary):
        print(f"Initializing Person({name}, {age}, {salary}")
        self.name = name
        self.age = age
        self.salary = salary

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r}, {self.age}, {self.salary})"


if __name__ == "__main__":
    bob = Person("Bob", 37, 12000)
    print(bob)
    Person("Bob", 38, 12000)
    Person("Bob", 38, 12000)
