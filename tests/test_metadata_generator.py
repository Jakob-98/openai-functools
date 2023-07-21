import pytest

from openai_functools.metadata_generator import openai_function, extract_openai_function_metadata

def test_extract_function_metadata(weather_function, expected_metadata):
    """Test that the metadata extraction produces the correct output."""
    metadata = extract_openai_function_metadata(weather_function)
    assert (
        metadata == expected_metadata
    ), f"Expected {expected_metadata}, but got {metadata}"

def test_function_metadata_decorator(weather_function, expected_metadata):
    """Test that the decorator correctly adds metadata to the function."""
    decorated_function = openai_function(weather_function)

    # Call the function to generate the metadata
    decorated_function("foo")

    assert (
        decorated_function.openai_metadata == expected_metadata
    ), f"Expected {expected_metadata}, but got {decorated_function.openai_metadata}"

def test_no_docstring_metadata_decorator(no_docstring_function, expected_no_docstring_metadata):
    """Test that the decorator can handle functions without docstrings."""
    decorated_function = openai_function(no_docstring_function)
    decorated_function("foo")
    assert (
        decorated_function.openai_metadata == expected_no_docstring_metadata
    ), f"Expected {expected_no_docstring_metadata}, but got {decorated_function.openai_metadata}"

def test_no_parameters_metadata_decorator(no_parameters_function, expected_no_parameters_metadata):
    """Test that the decorator can handle functions without parameters."""
    decorated_function = openai_function(no_parameters_function)
    decorated_function()
    assert (
        decorated_function.openai_metadata == expected_no_parameters_metadata
    ), f"Expected {expected_no_parameters_metadata}, but got {decorated_function.openai_metadata}"
