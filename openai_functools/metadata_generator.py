import inspect
from typing import Any, Callable
from functools import wraps
import re
from typing import Any, Callable, List
from openai_functools.types import python_type_to_openapi_type


def function_metadata_decorator(func: Callable) -> Callable:
    func.metadata = extract_function_metadata(func)

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    return wrapper


def extract_function_metadata(func: Callable) -> dict:
    sig = inspect.signature(func)
    params = sig.parameters
    properties = {}

    # parse the function's docstring
    docstring = func.__doc__
    docstring_dict = {}

    # TODO use docstring_parser instead, this is not a good way to parse docstrings
    if docstring:
        # we're assuming each parameter description is a separate line
        # that starts with the parameter's name, followed by a colon
        lines = docstring.split("\n")
        for line in lines:
            match = re.match(r"^\s*(\w+)\s*:\s*(.+)$", line)
            if match:
                param_name, param_desc = match.groups()
                docstring_dict[param_name] = param_desc.strip()

    for name, param in params.items():
        properties[name] = {
            "type": python_type_to_openapi_type(param.annotation)
            if param.annotation != param.empty
            else "string"
        }
        print(params, name)
        if name in docstring_dict:
            properties[name]["description"] = docstring_dict[name]
        else:
            properties[name]["description"] = name
        if param.default != param.empty:
            properties[name]["default"] = param.default

    print(func.__name__)
    metadata = {
        "name": func.__name__,
        "description": docstring.split("\n")[0] if docstring else func.__name__,
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": [
                name for name, param in params.items() if param.default == param.empty
            ],
        },
    }
    return metadata
