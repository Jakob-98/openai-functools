import pytest

from openai_functools.metadata_generator import (openai_function,
                                                 extract_openai_function_metadata)


def test_extract_function_metadata(weather_function, expected_metadata):
    metadata = extract_openai_function_metadata(weather_function)
    assert (
        metadata == expected_metadata
    ), f"Expected {expected_metadata}, but got {metadata}"


def test_function_metadata_decorator(weather_function, expected_metadata):
    decorated_function = openai_function(weather_function)

    # Call the function to generate the metadata
    decorated_function("foo")

    assert (
        decorated_function.openai_metadata == expected_metadata
    ), f"Expected {expected_metadata}, but got {decorated_function.openai_metadata}"
