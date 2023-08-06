from abc import ABC
from .type_ import Type


class BuiltInType(Type, ABC):

    def __init__(self, type_):
        self.type_ = type_

    def __call__(self, arg):
        return self.type_(arg)

    def recursive_children(self):
        return []

    @property
    def self_description(self):
        return f"{self.type_.__name__}"


class Str(BuiltInType):
    @property
    def simple_description(self):
        return "a string"

    @property
    def regex(self):
        return r'"([^"]*)"'


class Bool(BuiltInType):
    @property
    def simple_description(self):
        return "a boolean"

    @property
    def regex(self):
        return r"(true|false)"


class Float(BuiltInType):
    @property
    def simple_description(self):
        return "a float"

    @property
    def regex(self):
        return r"(\d+|\d*\.\d+(?!\d))"


class Int(BuiltInType):
    @property
    def simple_description(self):
        return "an integer"

    @property
    def regex(self):
        return r"(\d+)"
