class Simple:
    def __init__(self, argument: float):
        self.argument = argument

    def __eq__(self, other):
        if not isinstance(other, Simple):
            return False
        return self.argument == other.argument

    def __repr__(self):
        return f"Simple({self.argument})"


class Types:
    def __init__(
            self,
            int_argument: int,
            string_argument: str,
            boolean_argument: bool,
            float_argument: float,
    ):
        self.int_argument = int_argument
        self.string_argument = string_argument
        self.boolean_argument = boolean_argument
        self.float_argument = float_argument

    def __eq__(self, other):
        if not isinstance(other, Types):
            return False
        return (
                self.int_argument == other.int_argument
                and self.string_argument == other.string_argument
                and self.boolean_argument == other.boolean_argument
                and self.float_argument == other.float_argument
        )

    def __repr__(self):
        return f"Types({self.int_argument}, {self.string_argument}, {self.boolean_argument}, {self.float_argument})"


class Nested:
    def __init__(self, simple: Simple):
        self.simple = simple

    def __eq__(self, other):
        if not isinstance(other, Nested):
            return False
        return self.simple == other.simple

    def __repr__(self):
        return f"Nested({self.simple})"
