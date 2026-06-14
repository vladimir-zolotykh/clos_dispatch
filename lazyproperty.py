#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import math


class lazyproperty:
    def __init__(self, func):
        self.func = func
        self.cache = func.__name__ + "_cache"

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        if hasattr(instance, self.cache):
            return getattr(instance, self.cache)
        res = self.func(instance)
        setattr(instance, self.cache, res)
        return res


class Circle:
    def __init__(self, radius):
        self.radius = radius

    @lazyproperty
    def area(self):
        print("Calculating area")
        return math.pi * self.radius**2

    @lazyproperty
    def circumference(self):
        print("Calculating circumference")
        return 2 * math.pi * self.radius


if __name__ == "__main__":
    c = Circle(12.3)
    print(vars(c))
    print(c.area)
    print(vars(c))
    print(c.circumference)
    print(c.area)
