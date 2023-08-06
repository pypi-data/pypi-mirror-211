import json
from abc import ABC, abstractmethod
from inspect import isclass


class Type(ABC):
    """
    Any type that might be returned by a call to the LLM
    """
    @property
    @abstractmethod
    def regex(self) -> str:
        """
        A regular expression used by ReLLM to constrain the output such that it can
        be parsed as this type
        """

    @abstractmethod
    def __call__(self, response) -> object:
        """
        Convert the response into the appropriate type. The response conforms to the
        regex defined by this type
        """

    def from_json(self, response: str) -> object:
        """
        Convert a JSON string returned by the model into the appropriate type
        """
        return self.__call__(json.loads(response))

    def __new__(cls, type_):
        """
        Wrap a type in a Type object.

        Only supports some built-in types and classes with type annotations

        Parameters
        ----------
        type_
            The type to wrap
        """
        from .built_in_type import Int, Float, Bool, Str
        from .collection import List
        from .class_ import Class

        type_map = {
            int: Int,
            float: Float,
            bool: Bool,
            str: Str,
            list: List
        }

        try:
            return object.__new__(type_map[type_])
        except KeyError:
            if isclass(type_):
                return object.__new__(Class)

        raise TypeError(f"Type {type_} not supported")

    @abstractmethod
    def recursive_children(self):
        pass

    @property
    @abstractmethod
    def simple_description(self):
        pass

    @property
    def description(self):
        return "\n\n".join(child.self_description for child in self.recursive_children())

    @property
    @abstractmethod
    def self_description(self):
        pass
