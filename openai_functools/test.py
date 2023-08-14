import inspect
from typing import Literal
import typing
from enum  import Enum


class MyEnum(Enum):
    foo = "foo"
    bar = "bar"
    hello = "hello"
    goodbuy = "goodbuy"


def literal_function(string_literal: MyEnum) -> str:
    return string_literal


def literal_function_two(string_literal: str = Literal["foo", "bar", "hello", "goodbuy"]) -> str:
    return string_literal


def extract_literal_allowed_values(func):
    signature = inspect.signature(func)
    literal_parameters = {}

    for param_name, param in signature.parameters.items():

        if isinstance(param.default, typing._LiteralGenericAlias):
            literal_parameters[param_name] = list(param.default.__args__)

    return literal_parameters


if __name__ == "__main__":
    literal_allowed_values_dict = extract_literal_allowed_values(literal_function)

    for param_name, values in literal_allowed_values_dict.items():
        print(
            f"Parameter '{param_name}' has allowed Enum: {values}")

    literal_allowed_values_dict = extract_literal_allowed_values(literal_function_two)

    for param_name, values in literal_allowed_values_dict.items():
        print(
            f"Parameter '{param_name}' has allowed Enum: {values}")