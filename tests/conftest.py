from pytest import fixture


@fixture
def weather_function():
    def get_current_weather(location, unit="fahrenheit"):
        weather_info = {
            "location": location,
            "temperature": "72",
            "unit": unit,
            "forecast": ["sunny", "windy"],
        }
        return json.dumps(weather_info)

    return get_current_weather


@fixture()
def expected_metadata():
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
