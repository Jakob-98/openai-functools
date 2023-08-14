import inspect
import typing
from functools import wraps
from typing import Any, Callable, get_type_hints

from docstring_parser import parse

from openai_functools.types import python_type_to_openapi_type


def openai_function(func: Callable) -> Callable:
    func.openai_metadata = extract_openai_function_metadata(func)

    print(get_type_hints(func))

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    return wrapper


def extract_openai_function_metadata(func: Callable) -> dict:
    sig = inspect.signature(func)
    params = sig.parameters
    properties = {}

    # assumes the format from https://pypi.org/project/docstring-parser/
    docstring = parse(func.__doc__ if func.__doc__ else "")
    docstring_params = {param.arg_name: param.description for param in docstring.params}

    for name, param in params.items():
        properties[name] = extract_parameter_properties(param, docstring_params)

    metadata = {
        "name": func.__name__,
        "description": docstring.short_description or func.__name__,
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": [
                name for name, param in params.items() if param.default == param.empty
            ],
        },
    }
    return metadata


def extract_literal_allowed_values(func):
    signature = inspect.signature(func)
    literal_parameters = {}

    for param_name, param in signature.parameters.items():

        if isinstance(param.default, typing._LiteralGenericAlias):
            literal_parameters[param_name] = list(param.default.__args__)

    return literal_parameters


def extract_parameter_properties(
    param: inspect.Parameter, docstring_params: dict
) -> dict:
    name = param.name

    properties = {
        "type": python_type_to_openapi_type(param.annotation)
        if param.annotation != param.empty
        else "string"  # make this configurable?
    }

    properties["description"] = docstring_params.get(name, name)

    if isinstance(param.default, typing._LiteralGenericAlias):
        properties["enum"] = list(param.default.__args__)
        properties["default"] = param.default.__args__[0]
    else:
        if param.default != param.empty:
            properties["default"] = param.default

    return properties
