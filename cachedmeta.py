#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from collections import defaultdict
from dataclasses import dataclass


class CachedMeta(type):
    _cache = defaultdict(defaultdict)

    def __call__(cls, *args, **kwds):
        key = tuple(args)
        if cls not in (ca := type(cls)._cache) or key not in ca[cls]:
            ca[cls][key] = super().__call__(*args, **kwds)
        return ca[cls][key]


@dataclass
class Person(metaclass=CachedMeta):
    name: str
    age: int
    salary: float

    def __post_init__(self):
        print(f"Initializing Person({self.name}, {self.age}, {self.salary}")


def test_person(capsys):
    bob = Person("Bob", 37, 12000)
    print(bob)
    out = capsys.readouterr().out
    assert out.count("Initializing Person(Bob, 37, 12000") == 1
    assert "Initializing Person(Bob, 37, 12000" in out
    Person("Bob", 38, 12000)
    Person("Bob", 38, 12000)
    out = capsys.readouterr().out
    assert out.count("Initializing Person(Bob, 38, 12000") == 1


if __name__ == "__main__":
    import sys
    import pytest

    pytest.main(sys.argv)
