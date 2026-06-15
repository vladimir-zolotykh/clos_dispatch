#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from collections import defaultdict


class CachedMeta(type):
    _cache = defaultdict(defaultdict)

    def __call__(cls, *args, **kwds):
        key = tuple(args)
        if cls not in type(cls)._cache or key not in type(cls)._cache[cls]:
            type(cls)._cache[cls][key] = super().__call__(*args, **kwds)
        return type(cls)._cache[cls][key]


class Person(metaclass=CachedMeta):
    def __init__(self, name, age, salary):
        print(f"Initializing Person({name}, {age}, {salary}")
        self.name = name
        self.age = age
        self.salary = salary


if __name__ == "__main__":
    bob = Person("Bob", 37, 12000)
    print(bob)
    Person("Bob", 38, 12000)
    Person("Bob", 38, 12000)
