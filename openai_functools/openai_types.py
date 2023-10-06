"""Types module for openapi_functools """


def python_type_to_openapi_type(python_type: type) -> str:
    if python_type == str:
        return "string"
    elif python_type == int:
        return "integer"
    elif python_type == float:
        return "number"
    elif python_type == bool:
        return "boolean"
    elif python_type == list:
        return "array"
    elif python_type == dict:
        return "object"
    else:
        return "string"  # default
