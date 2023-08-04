import inspect
import logging
from functools import wraps
from typing import Any, Callable

from docstring_parser import parse

from openai_functools.types import python_type_to_openapi_type


def openai_function(func: Callable) -> Callable:
    logging.info(f"Called openai_function with function {func.__name__}")
    func.openai_metadata = extract_openai_function_metadata(func)

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    logging.info(f"Completed openai_function with function {func.__name__}")
    return wrapper


def extract_openai_function_metadata(func: Callable) -> dict:
    logging.info(f"Called extract_openai_function_metadata with function {func.__name__}")
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
    logging.info(f"Completed extract_openai_function_metadata with function {func.__name__}")
    return metadata


def extract_parameter_properties(
    param: inspect.Parameter, docstring_params: dict
) -> dict:
    logging.info(f"Called extract_parameter_properties with parameter {param.name}")
    name = param.name
    properties = {
        "type": python_type_to_openapi_type(param.annotation)
        if param.annotation != param.empty
        else "string"  # make this configurable?
    }
    properties["description"] = docstring_params.get(name, name)
    if param.default != param.empty:
        properties["default"] = param.default
    logging.info(f"Completed extract_parameter_properties with parameter {param.name}")
    return properties
