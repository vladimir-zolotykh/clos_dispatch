#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest
import sys


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwds):
        if cls not in (d := type(cls)._instances):
            d[cls] = super().__call__(*args, **kwds)
        return d[cls]


class Logger(metaclass=Singleton):
    def __init__(self):
        print(f"Initializing {self.__class__.__name__}")


class Module(metaclass=Singleton):
    def __init__(self):
        print(f"Initializing {self.__class__.__name__}")


def test_singleton():
    g1 = Logger()
    g2 = Logger()
    assert g1 is g2
    m1 = Module()
    m2 = Module()
    assert m1 is m2


if __name__ == "__main__":
    pytest.main(sys.argv)
