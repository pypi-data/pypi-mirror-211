from typing import Union, Callable

from regex import regex
from rellm import complete_re
from transformers import PreTrainedTokenizer, PreTrainedModel

from orellm.type_ import Type


def complete_object(
        prompt: str, tokenizer: PreTrainedTokenizer,
        return_type: Union[Type, type],
        model: PreTrainedModel,
        max_new_tokens: int = 800,
        complete_function: Callable = complete_re,
        generate_prompt=False,
        **model_kwargs,
):
    """
    Create an instance of a class from a prompt

    Parameters
    ----------
    prompt
        A natural language prompt to give to the model
    tokenizer
    return_type
        The type that should be returned
    model
        A Large Language Model
    max_new_tokens
        The maximum number of tokens to generate
    complete_function
        A function that produces LLM output constrained by a regex pattern (e.g. complete_re from ReLLM)
    model_kwargs
        Additional arguments to pass to the model
    generate_prompt
        Whether to generate a prompt from the return type

    Returns
    -------
    An instance of the class specified by return_type
    """
    if not isinstance(return_type, Type):
        return_type = Type(return_type)

    prefix = return_type.description if generate_prompt else ""

    pattern = regex.compile(return_type.regex)
    response = complete_function(
        tokenizer=tokenizer,
        model=model,
        prompt=f"{prefix}\n\n{prompt}",
        pattern=pattern,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        **model_kwargs
    )
    return return_type.from_json(response)
