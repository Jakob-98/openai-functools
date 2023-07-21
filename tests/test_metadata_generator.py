import pytest
from openai_functools.metadata_generator import (
    function_metadata_decorator,
    extract_function_metadata,
)


def test_extract_function_metadata(weather_function, expected_metadata):
    decorated_function = function_metadata_decorator(weather_function)
    metadata = decorated_function.metadata
    assert (
        metadata == expected_metadata
    ), f"Expected {expected_metadata}, but got {metadata}"


def test_function_metadata_decorator(weather_function, expected_metadata):
    decorated_function = function_metadata_decorator(weather_function)
    assert hasattr(
        decorated_function, "metadata"
    ), "Metadata attribute not found in the decorated function"
    assert (
        decorated_function.metadata == expected_metadata
    ), f"Expected {expected_metadata}, but got {decorated_function.metadata}"
