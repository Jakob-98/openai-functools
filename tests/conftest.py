import json
from enum import Enum
from typing import Literal

from pytest import fixture
from unittest.mock import MagicMock


@fixture
def weather_function():
    def get_current_weather(location: str, unit: str = "fahrenheit") -> str:
        """
        Get current weather.

        :param str location: The location to get the weather for.
        :param str unit: The unit for temperature, default is "fahrenheit".
        :return: A string containing the weather info.
        :rtype: str
        """
        weather_info = {
            "location": location,
            "temperature": "72",
            "unit": unit,
            "forecast": ["sunny", "windy"],
        }
        return json.dumps(weather_info)

    return get_current_weather


class Duck:
    """A Duck class"""

    def quack(self, someParam: str):
        return "Quack!"


@fixture
def duck_class_ref():
    return Duck


@fixture
def no_docstring_function():
    """Example function without docstrings."""

    def get_current_weather(location, unit="fahrenheit"):
        weather_info = {
            "location": location,
            "temperature": "72",
            "unit": unit,
            "forecast": ["sunny", "windy"],
        }
        return json.dumps(weather_info)

    return get_current_weather


@fixture
def no_parameters_function():
    """Example function without parameters."""

    def say_hello():
        return "Hello, world!"

    return say_hello


@fixture()
def expected_metadata():
    """Expected metadata for the weather_function fixture."""
    return {
        "name": "get_current_weather",
        "description": "Get current weather.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location to get the weather for.",
                },
                "unit": {
                    "type": "string",
                    "description": 'The unit for temperature, default is "fahrenheit".',
                    "default": "fahrenheit",
                },
            },
            "required": ["location"],
        },
    }


@fixture
def expected_no_docstring_metadata():
    """Expected metadata for the no_docstring_function fixture."""
    return {
        "name": "get_current_weather",
        "description": "get_current_weather",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "location"},
                "unit": {
                    "type": "string",
                    "description": "unit",
                    "default": "fahrenheit",
                },
            },
            "required": ["location"],
        },
    }


@fixture()
def weather_chat_response():
    mock_response = MagicMock()
    mock_response.choices[0].message.function_call.name = "get_current_weather"
    mock_response.choices[0].message.function_call.arguments = '{\n  "location": "Boston"\n}'
    return mock_response


@fixture
def expected_no_parameters_metadata():
    """Expected metadata for the no_parameters_function fixture."""
    return {
        "name": "say_hello",
        "description": "say_hello",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    }


@fixture
def function_with_literal():
    def literal_function(string_literal: str = Literal["foo", "bar"]) -> str:
        return f"Hello, {string_literal}!"

    return literal_function


@fixture
def expected_function_with_literal_metadata():
    return {
        "name": "literal_function",
        "description": "literal_function",
        "parameters": {
            "type": "object",
            "properties": {
                "string_literal": {
                    "type": "string",
                    "description": "string_literal",
                    "enum": ["foo", "bar"],
                    "default": "foo",
                },
            },
            "required": [],
        },
    }
