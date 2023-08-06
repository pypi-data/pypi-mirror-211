# Python objects from Large Language Models

Get arbitrarily complex Python objects back in response to requests to Large Language Models. Inspired by and built using [ReLLM](https://github.com/r2d4/rellm).   
Constructor type annotations are used to generate Regex patterns that filter LLM output to ensure it can be parsed as the target type. They are also used to generate part of the prompt.

## Installation

```bash
pip install orellm
```

## Usage

Describe what you want the LLM to return by defining a class.

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

from orellm import complete_object

# Define a class using type annotations
class MyClass:
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
        
    def __repr__(self):
        return f"MyClass(int_argument={self.int_argument}, string_argument={self.string_argument}, boolean_argument={self.boolean_argument}, float_argument={self.float_argument})"


model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")


prompt = "Give an instance of MyClass"

# Pass the class along with the tokenizer, model, and prompt
output = complete_object(
    tokenizer=tokenizer,
    model=model,
    prompt=prompt,
    return_type=MyClass,
)

# The response is an instance of MyClass
print(output)
# > MyClass(int_argument=0, string_argument='Give an instance of MyClass', boolean_argument=False, float_argument=0.0)
```

This also works for nested classes.

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

from orellm import complete_object


class Simple:
    def __init__(self, argument: float):
        self.argument = argument

    def __repr__(self):
        return f"Simple({self.argument})"


class Nested:
    def __init__(self, simple: Simple):
        self.simple = simple

    def __repr__(self):
        return f"Nested({self.simple})"


model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")


prompt = "Give an instance of Nested"

# Pass the class along with the tokenizer, model, and prompt
output = complete_object(
    tokenizer=tokenizer,
    model=model,
    prompt=prompt,
    return_type=Nested,
)

# The response is an instance of Nested
print(output)
# > Nested(Simple(0.0))
```