import json

from pytest import fixture


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
